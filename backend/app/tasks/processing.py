from celery import Celery
from app.config import get_settings
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
import json

settings = get_settings()

celery_app = Celery(
    "audio_processor",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_timeout=1,
    broker_transport_options={
        "socket_connect_timeout": 1,
        "socket_timeout": 1,
    },
)


def _clamp_frequency(value: float, sample_rate: int) -> float:
    nyquist = sample_rate / 2
    return max(1.0, min(float(value), nyquist - 1.0))


def _apply_filter(audio_data, sample_rate: int, filter_type: str, params: dict):
    import numpy as np
    from scipy import signal

    if audio_data.ndim > 1:
        channels = [
            _apply_filter(audio_data[:, channel], sample_rate, filter_type, params)
            for channel in range(audio_data.shape[1])
        ]
        return np.stack(channels, axis=1)

    order = int(params.get("order", 5))
    order = max(1, min(order, 10))
    nyquist = sample_rate / 2

    if filter_type == "lowpass":
        cutoff = _clamp_frequency(params.get("cutoff_freq", 5000), sample_rate)
        b, a = signal.butter(order, cutoff / nyquist, btype="low")
        return signal.filtfilt(b, a, audio_data)

    if filter_type == "highpass":
        cutoff = _clamp_frequency(params.get("cutoff_freq", 300), sample_rate)
        b, a = signal.butter(order, cutoff / nyquist, btype="high")
        return signal.filtfilt(b, a, audio_data)

    if filter_type == "bandpass":
        low = _clamp_frequency(params.get("low_freq", 300), sample_rate)
        high = _clamp_frequency(params.get("high_freq", 3400), sample_rate)
        low, high = sorted((low, high))
        if high - low < 1:
            high = min(low + 1, nyquist - 1)
        b, a = signal.butter(order, [low / nyquist, high / nyquist], btype="band")
        return signal.filtfilt(b, a, audio_data)

    if filter_type == "notch":
        center = _clamp_frequency(params.get("center_freq", 60), sample_rate)
        quality = max(1.0, float(params.get("quality", 30.0)))
        b, a = signal.iirnotch(center, quality, sample_rate)
        return signal.filtfilt(b, a, audio_data)

    if filter_type == "fir":
        num_taps = int(params.get("num_taps", 101))
        if num_taps % 2 == 0:
            num_taps += 1
        num_taps = max(3, min(num_taps, 1001))
        cutoff = _clamp_frequency(params.get("cutoff_freq", 5000), sample_rate)
        taps = signal.firwin(num_taps, cutoff / nyquist)
        return signal.convolve(audio_data, taps, mode="same")

    if filter_type == "iir":
        cutoff = _clamp_frequency(params.get("cutoff_freq", 5000), sample_rate)
        b, a = signal.butter(order, cutoff / nyquist, btype="low")
        return signal.filtfilt(b, a, audio_data)

    raise ValueError(f"Unsupported filter type: {filter_type}")


def _apply_noise_reduction(audio_data, sample_rate: int):
    import numpy as np

    window_size = max(1, int(sample_rate * 0.05))
    if audio_data.ndim > 1:
        channels = [
            _apply_noise_reduction(audio_data[:, channel], sample_rate)
            for channel in range(audio_data.shape[1])
        ]
        return np.stack(channels, axis=1)

    kernel = np.ones(window_size) / window_size
    noise_floor = np.convolve(np.abs(audio_data), kernel, mode="same") * 0.25
    reduced = np.sign(audio_data) * np.maximum(np.abs(audio_data) - noise_floor, 0)
    return reduced


def _parse_filter_params(raw_params: str | None) -> dict:
    if not raw_params:
        return {}
    parsed = json.loads(raw_params)
    if not isinstance(parsed, dict):
        raise ValueError("Filter parameters must be a JSON object")
    return parsed


@celery_app.task(bind=True)
def process_audio_task(self, job_id: str):
    """
    Celery task to process audio asynchronously.
    
    Args:
        job_id: UUID of the processing job
    """
    from app.database import SessionLocal
    from app.models import AudioFile, JobStatus, ProcessingJob
    from app.services.storage import StorageService
    import numpy as np
    import soundfile as sf

    print(f"Processing job: {job_id}")
    db = SessionLocal()
    try:
        try:
            job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
            if job:
                job.status = JobStatus.PROCESSING
                job.progress = 10.0
                job.started_at = datetime.utcnow()
                db.commit()

                audio_file = db.query(AudioFile).filter(AudioFile.id == job.audio_file_id).first()
                if not audio_file:
                    raise ValueError("Audio file not found for processing job")

                storage = StorageService()
                input_bytes = storage.download_bytes(audio_file.file_path)
                params = _parse_filter_params(job.filter_params)

                with TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    input_path = temp_path / Path(audio_file.file_path).name
                    output_path = temp_path / f"processed-{Path(audio_file.filename).stem}.wav"
                    input_path.write_bytes(input_bytes)

                    audio_data, sample_rate = sf.read(input_path)
                    job.progress = 35.0
                    db.commit()

                    processed = _apply_filter(audio_data, sample_rate, job.filter_type, params)
                    if job.apply_noise_reduction == "true":
                        processed = _apply_noise_reduction(processed, sample_rate)

                    processed = np.clip(processed, -1.0, 1.0)
                    job.progress = 75.0
                    db.commit()

                    sf.write(output_path, processed, sample_rate)
                    output_file_path = storage.upload_bytes(
                        output_path.read_bytes(),
                        output_path.name,
                        content_type="audio/wav",
                    )

                job.output_file_path = output_file_path
                job.status = JobStatus.COMPLETED
                job.progress = 100.0
                job.completed_at = datetime.utcnow()
                job.error_message = None
                db.commit()

            return {"status": "completed", "job_id": job_id}
        except Exception as e:
            job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
            if job:
                job.status = JobStatus.FAILED
                job.error_message = str(e)
                job.completed_at = datetime.utcnow()
                db.commit()
            print(f"Error processing job {job_id}: {str(e)}")
            raise
    finally:
        db.close()

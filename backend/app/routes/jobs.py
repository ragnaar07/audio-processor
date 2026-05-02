from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from uuid import UUID
from socket import create_connection
from urllib.parse import urlparse
from app.database import get_db
from app.models import JobStatus, ProcessingJob
from app.schemas import ProcessingJobCreate, ProcessingJobResponse
from app.tasks.processing import process_audio_task

router = APIRouter(prefix="/api/jobs", tags=["processing"])


def celery_broker_available() -> bool:
    """Fast broker reachability check to avoid long Redis connection waits."""
    broker_url = process_audio_task.app.conf.broker_url
    parsed = urlparse(broker_url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 6379
    try:
        with create_connection((host, port), timeout=0.5):
            return True
    except OSError:
        return False


@router.post("/", response_model=ProcessingJobResponse)
async def create_processing_job(
    job_create: ProcessingJobCreate,
    db: Session = Depends(get_db)
):
    """Create a new audio processing job."""
    try:
        # Create job record
        job = ProcessingJob(
            audio_file_id=job_create.audio_file_id,
            filter_type=job_create.filter_type,
            filter_params=job_create.filter_params,
            apply_noise_reduction=str(job_create.apply_noise_reduction).lower(),
        )
        
        db.add(job)
        db.commit()
        db.refresh(job)
        
        # Queue Celery task when the broker is available. Local development can
        # still complete the placeholder job without Redis running.
        if celery_broker_available():
            task = process_audio_task.delay(str(job.id))
            job.celery_task_id = task.id
        else:
            process_audio_task.run(str(job.id))
            db.expire(job)

        db.commit()
        db.refresh(job)
        
        return job
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}", response_model=ProcessingJobResponse)
async def get_job_status(
    job_id: UUID,
    db: Session = Depends(get_db)
):
    """Get processing job status."""
    job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/{job_id}/download")
async def download_processed_audio(
    job_id: UUID,
    db: Session = Depends(get_db)
):
    """Download processed audio output for a completed job."""
    job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != JobStatus.COMPLETED or not job.output_file_path:
        raise HTTPException(status_code=404, detail="Processed audio is not available")

    from app.services.storage import StorageService

    storage = StorageService()
    content = storage.download_bytes(job.output_file_path)
    filename = job.output_file_path.split("/")[-1]
    return Response(
        content=content,
        media_type="audio/wav",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/", response_model=list[ProcessingJobResponse])
async def list_jobs(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List all processing jobs."""
    jobs = db.query(ProcessingJob).offset(skip).limit(limit).all()
    return jobs

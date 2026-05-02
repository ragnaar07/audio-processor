from sqlalchemy import CHAR, Column, String, DateTime, Float, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import TypeDecorator
from datetime import datetime
import uuid
from enum import Enum as PyEnum
from app.database import Base


class GUID(TypeDecorator):
    """Platform-independent UUID type.

    PostgreSQL stores UUIDs natively; SQLite stores them as 36-character strings.
    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID(as_uuid=True))
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name == "postgresql":
            return value if isinstance(value, uuid.UUID) else uuid.UUID(str(value))
        return str(value if isinstance(value, uuid.UUID) else uuid.UUID(str(value)))

    def process_result_value(self, value, dialect):
        if value is None or isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(str(value))


class JobStatus(str, PyEnum):
    """Enum for job processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class FilterType(str, PyEnum):
    """Enum for filter types."""
    FIR = "fir"
    IIR = "iir"
    LOWPASS = "lowpass"
    HIGHPASS = "highpass"
    BANDPASS = "bandpass"
    NOTCH = "notch"


class AudioFile(Base):
    """Audio file metadata model."""
    __tablename__ = "audio_files"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)  # MinIO path
    file_size = Column(Integer, nullable=False)  # bytes
    duration = Column(Float, nullable=False)  # seconds
    sample_rate = Column(Integer, nullable=False)  # Hz
    channels = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProcessingJob(Base):
    """Audio processing job model."""
    __tablename__ = "processing_jobs"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    audio_file_id = Column(GUID(), nullable=False, index=True)
    celery_task_id = Column(String(255), nullable=True, unique=True)
    
    # Processing parameters
    filter_type = Column(String(50), nullable=False)
    filter_params = Column(String(1000), nullable=True)  # JSON string
    apply_noise_reduction = Column(String(10), default="false")
    
    # Results
    output_file_path = Column(String(500), nullable=True)  # MinIO path
    
    # Status
    status = Column(String(50), default=JobStatus.PENDING, index=True)
    progress = Column(Float, default=0.0)  # 0-100%
    error_message = Column(String(500), nullable=True)
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

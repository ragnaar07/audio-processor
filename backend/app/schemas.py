from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


# Audio File Schemas
class AudioFileBase(BaseModel):
    filename: str
    duration: float
    sample_rate: int
    channels: int


class AudioFileCreate(AudioFileBase):
    pass


class AudioFileResponse(AudioFileBase):
    id: UUID
    file_path: str
    file_size: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Processing Job Schemas
class ProcessingJobBase(BaseModel):
    audio_file_id: UUID
    filter_type: str
    filter_params: Optional[str] = None
    apply_noise_reduction: bool = False


class ProcessingJobCreate(ProcessingJobBase):
    pass


class ProcessingJobResponse(ProcessingJobBase):
    id: UUID
    celery_task_id: Optional[str]
    status: str
    progress: float
    error_message: Optional[str]
    output_file_path: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ProcessingJobUpdate(BaseModel):
    status: Optional[str] = None
    progress: Optional[float] = None
    error_message: Optional[str] = None


# Health Check
class HealthResponse(BaseModel):
    status: str
    database: str
    redis: str
    s3: str

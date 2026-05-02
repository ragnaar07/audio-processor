from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AudioFile
from app.schemas import AudioFileResponse
from app.services.storage import StorageService
from datetime import datetime

router = APIRouter(prefix="/api/audio", tags=["audio"])

storage_service = StorageService()


@router.post("/upload", response_model=AudioFileResponse)
async def upload_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and store audio file."""
    try:
        # Validate file type
        filename = file.filename or ""
        if not filename.lower().endswith(('.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac')):
            raise HTTPException(status_code=400, detail="Invalid audio file format")
        
        # Upload to MinIO
        file_path = await storage_service.upload_file(file)
        
        # Extract audio metadata
        duration, sample_rate, channels = await storage_service.get_audio_metadata(file_path)
        
        # Create database record
        audio_file = AudioFile(
            filename=file.filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file.size or 0,
            duration=duration,
            sample_rate=sample_rate,
            channels=channels,
            created_at=datetime.utcnow(),
        )
        
        db.add(audio_file)
        db.commit()
        db.refresh(audio_file)
        
        return audio_file
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{file_id}", response_model=AudioFileResponse)
async def get_audio_file(
    file_id: str,
    db: Session = Depends(get_db)
):
    """Get audio file information."""
    audio_file = db.query(AudioFile).filter(AudioFile.id == file_id).first()
    if not audio_file:
        raise HTTPException(status_code=404, detail="Audio file not found")
    return audio_file

import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile
from app.config import get_settings
import os
from pathlib import Path
from uuid import uuid4
from typing import Optional

settings = get_settings()


class StorageService:
    """Service for handling file storage operations."""
    
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.MINIO_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name="us-east-1",
        )
        self.bucket = settings.AWS_S3_BUCKET
        self.local_root = Path(__file__).resolve().parents[2] / "local_storage"
        self.use_local_storage = False

        try:
            self.s3_client.head_bucket(Bucket=self.bucket)
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            if error_code in {"404", "NoSuchBucket"}:
                try:
                    self.s3_client.create_bucket(Bucket=self.bucket)
                except ClientError as create_error:
                    create_error_code = create_error.response.get("Error", {}).get("Code")
                    if create_error_code != "BucketAlreadyOwnedByYou":
                        raise
            else:
                self._enable_local_storage()
        except Exception:
            self._enable_local_storage()

    def _enable_local_storage(self) -> None:
        """Use local files when S3 is unavailable, mainly for local development."""
        if not self.use_local_storage:
            print("⚠️  MinIO/S3 not available, using local file storage instead")
            self.use_local_storage = True
            (self.local_root / "audio").mkdir(parents=True, exist_ok=True)
            (self.local_root / "processed").mkdir(parents=True, exist_ok=True)
    
    async def upload_file(self, file: UploadFile) -> str:
        """
        Upload file to MinIO/S3.
        
        Returns:
            str: Path to uploaded file
        """
        try:
            content = await file.read()
            safe_filename = Path(file.filename or "audio").name
            file_path = f"audio/{uuid4()}-{safe_filename}"

            if self.use_local_storage:
                destination = self.local_root / file_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(content)
                return file_path
            
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=file_path,
                Body=content,
                ContentType=file.content_type,
            )
            
            return file_path
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")

    def upload_bytes(
        self,
        content: bytes,
        filename: str,
        content_type: str = "application/octet-stream",
        folder: str = "processed",
    ) -> str:
        """Upload generated content to storage."""
        try:
            safe_filename = Path(filename).name
            file_path = f"{folder}/{uuid4()}-{safe_filename}"

            if self.use_local_storage:
                destination = self.local_root / file_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(content)
                return file_path

            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=file_path,
                Body=content,
                ContentType=content_type,
            )
            return file_path
        except Exception as e:
            raise Exception(f"Failed to upload generated file: {str(e)}")
    
    async def get_audio_metadata(self, file_path: str):
        """
        Extract audio metadata.
        
        Returns:
            tuple: (duration, sample_rate, channels)
        """
        try:
            import soundfile as sf
            
            if self.use_local_storage:
                temp_path = self.local_root / file_path
            else:
                # Download file temporarily
                obj = self.s3_client.get_object(Bucket=self.bucket, Key=file_path)
                audio_data = obj['Body'].read()
                
                # Save temporarily
                temp_path = Path("/tmp") / file_path.split("/")[-1]
                temp_path.write_bytes(audio_data)
            
            # Extract metadata
            info = sf.info(temp_path)
            duration = info.frames / info.samplerate if info.samplerate else 0
            sample_rate = info.samplerate
            channels = info.channels
            
            # Cleanup
            if not self.use_local_storage:
                os.remove(temp_path)
            
            return duration, sample_rate, channels
        except Exception as e:
            raise Exception(f"Failed to extract audio metadata: {str(e)}")
    
    async def download_file(self, file_path: str) -> bytes:
        """Download file from MinIO/S3."""
        return self.download_bytes(file_path)

    def download_bytes(self, file_path: str) -> bytes:
        """Download file content from MinIO/S3 or local storage."""
        try:
            if self.use_local_storage:
                return (self.local_root / file_path).read_bytes()

            obj = self.s3_client.get_object(Bucket=self.bucket, Key=file_path)
            return obj['Body'].read()
        except Exception as e:
            raise Exception(f"Failed to download file: {str(e)}")
    
    def delete_file(self, file_path: str) -> bool:
        """Delete file from MinIO/S3."""
        try:
            if self.use_local_storage:
                path = self.local_root / file_path
                if path.exists():
                    path.unlink()
                return True

            self.s3_client.delete_object(Bucket=self.bucket, Key=file_path)
            return True
        except Exception as e:
            raise Exception(f"Failed to delete file: {str(e)}")

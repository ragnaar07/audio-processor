# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### Health Check

#### GET /health
Check API health status.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "environment": "development",
  "database": "connected",
  "redis": "connected",
  "s3": "connected"
}
```

---

## Audio File Management

### Upload Audio

#### POST /api/audio/upload
Upload an audio file.

**Request**:
- Content-Type: `multipart/form-data`
- Body:
  - `file` (File): Audio file (MP3, WAV, FLAC, OGG)

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "sample.wav",
  "file_path": "audio/sample.wav",
  "file_size": 1048576,
  "duration": 30.5,
  "sample_rate": 44100,
  "channels": 2,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors**:
- 400: Invalid audio format
- 500: Upload failed

---

### Get Audio File

#### GET /api/audio/{file_id}
Retrieve audio file information.

**Parameters**:
- `file_id` (UUID): File ID

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "sample.wav",
  "file_path": "audio/sample.wav",
  "file_size": 1048576,
  "duration": 30.5,
  "sample_rate": 44100,
  "channels": 2,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors**:
- 404: File not found

---

## Processing Jobs

### Create Processing Job

#### POST /api/jobs/
Create a new audio processing job.

**Request Body**:
```json
{
  "audio_file_id": "550e8400-e29b-41d4-a716-446655440000",
  "filter_type": "lowpass",
  "filter_params": "{\"cutoff_freq\": 5000}",
  "apply_noise_reduction": false
}
```

**Parameters**:
- `audio_file_id` (UUID): ID of uploaded audio file
- `filter_type` (string): Type of filter (lowpass, highpass, bandpass, notch, fir, iir)
- `filter_params` (string): JSON string with filter parameters
- `apply_noise_reduction` (boolean): Apply noise reduction

**Response** (201 Created):
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440111",
  "audio_file_id": "550e8400-e29b-41d4-a716-446655440000",
  "celery_task_id": "task-12345",
  "filter_type": "lowpass",
  "filter_params": "{\"cutoff_freq\": 5000}",
  "status": "pending",
  "progress": 0,
  "error_message": null,
  "output_file_path": null,
  "created_at": "2024-01-15T10:31:00Z",
  "started_at": null,
  "completed_at": null
}
```

**Errors**:
- 400: Invalid parameters
- 500: Job creation failed

---

### Get Job Status

#### GET /api/jobs/{job_id}
Retrieve processing job status.

**Parameters**:
- `job_id` (UUID): Job ID

**Response** (200 OK):
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440111",
  "audio_file_id": "550e8400-e29b-41d4-a716-446655440000",
  "celery_task_id": "task-12345",
  "filter_type": "lowpass",
  "filter_params": "{\"cutoff_freq\": 5000}",
  "status": "processing",
  "progress": 45,
  "error_message": null,
  "output_file_path": null,
  "created_at": "2024-01-15T10:31:00Z",
  "started_at": "2024-01-15T10:31:05Z",
  "completed_at": null
}
```

**Statuses**:
- `pending`: Waiting to be processed
- `processing`: Currently being processed
- `completed`: Processing finished successfully
- `failed`: Processing failed

**Errors**:
- 404: Job not found

---

### List Jobs

#### GET /api/jobs/
List all processing jobs.

**Query Parameters**:
- `skip` (integer): Number of jobs to skip (default: 0)
- `limit` (integer): Number of jobs to return (default: 10)

**Response** (200 OK):
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440111",
    "audio_file_id": "550e8400-e29b-41d4-a716-446655440000",
    "celery_task_id": "task-12345",
    "filter_type": "lowpass",
    "filter_params": "{\"cutoff_freq\": 5000}",
    "status": "completed",
    "progress": 100,
    "error_message": null,
    "output_file_path": "output/result.wav",
    "created_at": "2024-01-15T10:31:00Z",
    "started_at": "2024-01-15T10:31:05Z",
    "completed_at": "2024-01-15T10:31:30Z"
  }
]
```

---

## Filter Types & Parameters

### Lowpass Filter
```json
{
  "filter_type": "lowpass",
  "filter_params": "{\"cutoff_freq\": 5000, \"order\": 5}"
}
```
- `cutoff_freq`: Cutoff frequency in Hz
- `order`: Filter order (default: 5)

### Highpass Filter
```json
{
  "filter_type": "highpass",
  "filter_params": "{\"cutoff_freq\": 100, \"order\": 5}"
}
```

### Bandpass Filter
```json
{
  "filter_type": "bandpass",
  "filter_params": "{\"low_freq\": 300, \"high_freq\": 3400, \"order\": 5}"
}
```

### Notch Filter
```json
{
  "filter_type": "notch",
  "filter_params": "{\"center_freq\": 60, \"quality\": 30}"
}
```

### FIR Filter
```json
{
  "filter_type": "fir",
  "filter_params": "{\"num_taps\": 101}"
}
```

### IIR Filter
```json
{
  "filter_type": "iir",
  "filter_params": "{\"cutoff_freq\": 5000}"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid audio format"
}
```

### 404 Not Found
```json
{
  "detail": "Audio file not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to upload file"
}
```

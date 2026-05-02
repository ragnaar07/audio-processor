# Project Architecture

## System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                      │
│  - React Components (Material-UI)                              │
│  - Audio Upload, Visualization, Controls                       │
│  - Real-time Status Updates                                    │
└───────────────┬─────────────────────────────────────────────────┘
                │ HTTP/WebSocket
┌───────────────▼─────────────────────────────────────────────────┐
│                      FastAPI Backend                            │
│  - REST API Endpoints                                          │
│  - Request Validation (Pydantic)                               │
│  - Database Models (SQLAlchemy)                                │
│  - Job Queue Integration                                       │
└───────────────┬─────────────────────────────────────────────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌──────────┐
│PostgreSQL│ │ Redis  │ │ MinIO    │
│Database │ │ Cache  │ │ Storage  │
└────────┘ └────────┘ └──────────┘
                │
                ▼
        ┌──────────────────┐
        │  Celery Workers  │
        │  (DSP Tasks)     │
        └──────────────────┘
                │
                ▼
        ┌──────────────────┐
        │  DSP Engine      │
        │  (NumPy/SciPy)   │
        └──────────────────┘
```

## Components

### Frontend (Next.js + Material-UI)
- **Purpose**: User-facing interface for audio processing
- **Key Components**:
  - AudioUpload: Drag-and-drop file upload
  - WaveformVisualizer: Real-time audio visualization
  - ProcessingControls: Filter selection and configuration
  - JobStatus: Processing progress tracking

### Backend (FastAPI)
- **Purpose**: API server and job coordination
- **Responsibilities**:
  - Handle file uploads and storage
  - Create and manage processing jobs
  - Coordinate with Celery workers
  - Track job status and results
  - Database operations

### Database (PostgreSQL)
- **Purpose**: Persistent data storage
- **Tables**:
  - `audio_files`: Metadata for uploaded audio
  - `processing_jobs`: Job records and status

### Cache & Message Broker (Redis)
- **Purpose**: Celery message broker and caching
- **Functions**:
  - Task queue for async processing
  - Result backend for job outputs
  - Session caching (optional)

### Storage (MinIO)
- **Purpose**: S3-compatible file storage
- **Buckets**:
  - `audio-processor/audio`: Original uploaded audio
  - `audio-processor/output`: Processed audio results

### DSP Engine
- **Purpose**: Audio signal processing
- **Algorithms**:
  - FIR/IIR Filters (Low-pass, High-pass, Band-pass, Notch)
  - FFT Analysis
  - Noise Reduction
  - Audio I/O and metadata extraction

## Data Flow

### Upload & Processing
1. User uploads audio file via Frontend
2. Backend validates file and uploads to MinIO
3. Backend creates AudioFile record in PostgreSQL
4. Frontend displays waveform visualization
5. User selects processing options and submits job
6. Backend creates ProcessingJob and queues Celery task
7. Celery worker processes audio using DSP Engine
8. Results saved to MinIO and database updated
9. Frontend polls for status updates and displays progress

### Job Lifecycle
```
pending → processing → completed
  │                        ▲
  │                        │
  └─────────→ failed ──────┘
```

## Scaling Considerations

### Horizontal Scaling
- **API Servers**: Multiple FastAPI instances behind load balancer
- **Celery Workers**: Auto-scaling based on queue depth
- **Database**: Connection pooling and read replicas
- **Redis**: Sentinel for high availability

### Optimization
- Cache frequently accessed data (filter presets)
- Chunked audio processing for large files
- Compression for stored audio
- CDN for frontend assets

## Technology Stack Rationale

| Component | Technology | Why |
|-----------|-----------|-----|
| Frontend | Next.js | SSR, optimized builds, API routes option |
| UI Framework | Material-UI | Rich components, accessibility, theming |
| Audio Viz | WaveForm.js | Lightweight, good UX for waveforms |
| Backend | FastAPI | Performance, type safety, async support |
| Database | PostgreSQL | ACID compliance, JSON support, scalability |
| Cache | Redis | Fast in-memory ops, Celery integration |
| Storage | MinIO | Self-hosted S3-compatible, easy deployment |
| Task Queue | Celery | Distributed, reliable, scalable async tasks |
| DSP | NumPy/SciPy | Mature, optimized, industry-standard |

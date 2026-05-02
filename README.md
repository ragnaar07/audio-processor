# DSP Audio Processing Web App

A scalable full-stack web application for audio processing with DSP filters, signal visualization, and asynchronous task processing.

## Demo

Watch the project demo: https://youtu.be/tujRxVQT0xE

## 🏗️ Architecture

```
Client (Next.js) → API Gateway (FastAPI) → DSP Processing Service → Storage (MinIO/S3)
                                         ↓
                                    Database (PostgreSQL)
                                    Task Queue (Celery/Redis)
```

## 📁 Project Structure

```
audio-processor/
├── frontend/              # Next.js frontend (React + Material-UI)
├── backend/               # FastAPI backend
├── dsp-engine/            # DSP processing service
├── docker/                # Docker configs
├── docs/                  # Documentation
└── docker-compose.yml     # Services orchestration
```

## 🚀 Quick Start

### Fastest Way (Full Docker - Recommended for First Time)
```bash
cd /Users/aryannn/Desktop/audio-processor
chmod +x docker/start-prod.sh
./docker/start-prod.sh
```
Opens at: http://localhost:3000 (wait 10 seconds for services to start)

### Development Mode (Hot Reload - Recommended for Coding)
See **[QUICK_RUN.md](QUICK_RUN.md)** for 4-terminal setup with hot reload

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for manual frontend development)
- Python 3.9+ (for manual backend development)

### Complete Guide
For detailed instructions: **[RUN.md](RUN.md)**

## 📚 Key Technologies

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js, React, Material-UI, WaveForm.js |
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | PostgreSQL |
| Cache/Queue | Redis, Celery |
| Storage | MinIO (S3-compatible) |
| DSP | NumPy, SciPy, librosa |

## 🔄 Data Flow

1. User uploads audio → Backend stores & generates job ID
2. User selects processing options → Job queued to Celery
3. DSP worker processes audio asynchronously
4. Status updates in real-time
5. User downloads processed output

## 📝 Features

### Phase 1 (MVP)
- [x] Audio upload & storage
- [x] FIR filter implementation
- [x] Basic visualization
- [x] Async processing with Celery
- [x] Download processed audio

### Phase 2
- [ ] IIR filters
- [ ] FFT analysis
- [ ] Noise reduction
- [ ] Real-time waveform preview

### Phase 3
- [ ] User authentication
- [ ] Real-time streaming
- [ ] User dashboard
- [ ] Subscription model

## 🐳 Docker Services

- **PostgreSQL**: Database (port 5432)
- **Redis**: Cache & task queue (port 6379)
- **MinIO**: S3-compatible storage (port 9000, console 9001)
- **Celery**: Background task worker
- **FastAPI**: Backend API (port 8000)
- **Next.js**: Frontend (port 3000)

## 📖 Documentation

See [docs/](docs/) for detailed guides on:
- Architecture & design
- API endpoints
- DSP filter implementations
- Deployment

## 🛠️ Development

### Backend Development
```bash
cd backend
source venv/bin/activate
pytest  # Run tests
```

### Frontend Development
```bash
cd frontend
npm run dev  # Dev server
npm run lint # Linting
```

## 🚢 Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for:
- AWS deployment
- Vercel frontend hosting
- Scaling strategies

## 📄 License

MIT

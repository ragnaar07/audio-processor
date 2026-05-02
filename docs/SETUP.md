# Setup & Installation Guide

## Prerequisites

- **macOS 10.15+** (or Linux/Windows with minor adjustments)
- **Docker & Docker Compose** (latest version)
- **Node.js 18+** (`node --version`)
- **Python 3.9+** (`python3 --version`)
- **Git**

## Step 1: Clone & Setup Environment

```bash
cd /Users/aryannn/Desktop/audio-processor

# Copy environment file
cp .env.example .env
```

Edit `.env` and update any credentials if needed (defaults are fine for development).

## Step 2: Start Docker Services

```bash
# Start PostgreSQL, Redis, and MinIO
docker-compose up -d

# Verify services are running
docker-compose ps
```

Expected output:
```
NAME                        STATUS
audio-processor-postgres    Up (healthy)
audio-processor-redis       Up (healthy)
audio-processor-minio       Up (healthy)
```

**Access MinIO Console**: http://localhost:9001
- Username: `minioadmin`
- Password: `minioadmin`

## Step 3: Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database tables
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Start FastAPI server
python -m uvicorn main:app --reload
```

The backend will be available at: http://localhost:8000

**API Documentation**: http://localhost:8000/docs

## Step 4: Frontend Setup

In a new terminal:

```bash
cd frontend

# Copy environment file
cp .env.local.example .env.local

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at: http://localhost:3000

## Step 5: Celery Worker Setup (Optional)

In a new terminal:

```bash
cd backend

# Activate virtual environment
source venv/bin/activate

# Start Celery worker
celery -A app.tasks.processing worker --loglevel=info
```

## Verification

1. **Frontend**: Open http://localhost:3000
2. **Backend API**: Open http://localhost:8000/docs
3. **MinIO Console**: Open http://localhost:9001
4. **Database**: Check with `psql postgresql://audiouser:audiopass@localhost:5432/audiodb`

## Common Issues

### PostgreSQL Connection Error
```
Error: could not connect to database
```
**Solution**: Ensure `docker-compose up -d` completed and containers are healthy
```bash
docker-compose logs postgres
```

### Redis Connection Error
**Solution**: Check Redis is running
```bash
docker-compose logs redis
```

### Port Already in Use
**Solution**: Check what's using the port and either kill it or change docker-compose port
```bash
lsof -i :8000  # Check port 8000
lsof -i :3000  # Check port 3000
```

### MinIO Bucket Not Found
**Solution**: Create bucket manually via console or CLI
```bash
# Using AWS CLI with MinIO endpoint
aws s3 mb s3://audio-processor \
  --endpoint-url http://localhost:9000 \
  --region us-east-1
```

## Development Workflow

### Running Tests
```bash
cd backend
pytest
```

### Linting
```bash
cd frontend
npm run lint
```

### Database Migrations
```bash
# Using SQLAlchemy (manual for now)
cd backend
python -c "from app.database import Base, engine; Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)"
```

## Stopping Services

```bash
# Stop Docker services
docker-compose down

# Deactivate Python environment
deactivate
```

## Next Steps

1. Review [API.md](API.md) for endpoint documentation
2. Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design
3. Explore [DSP_FILTERS.md](DSP_FILTERS.md) for audio processing details
4. Deploy instructions in [DEPLOYMENT.md](DEPLOYMENT.md)

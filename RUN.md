# How to Run the Audio Processor Application

This guide covers all the different ways to run the application.

## 🚀 Quick Start (Recommended)

### Option 1: Docker (Production-like, Full Stack)

Fastest way to get everything running with all services in containers.

```bash
cd /Users/aryannn/Desktop/audio-processor
chmod +x docker/start-prod.sh
./docker/start-prod.sh
```

This starts:
- ✅ PostgreSQL (database)
- ✅ Redis (cache & task queue)
- ✅ MinIO (storage)
- ✅ FastAPI Backend
- ✅ Next.js Frontend
- ✅ Celery Worker

**Access:**
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- MinIO: http://localhost:9001

---

### Option 2: Development (Manual, Recommended for Development)

Best for active development with hot reload.

#### Step 1: Start Infrastructure Services
```bash
cd /Users/aryannn/Desktop/audio-processor
chmod +x docker/start-dev.sh
./docker/start-dev.sh
```

This starts only:
- PostgreSQL
- Redis
- MinIO

#### Step 2: Start Backend (Terminal 1)
```bash
cd /Users/aryannn/Desktop/audio-processor/backend

# Create virtual environment (first time only)
python3 -m venv venv

# Activate environment
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start server
python -m uvicorn main:app --reload
```

Output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

#### Step 3: Start Frontend (Terminal 2)
```bash
cd /Users/aryannn/Desktop/audio-processor/frontend

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

Output:
```
▲ Next.js 14.0.4
- Local:        http://localhost:3000
```

#### Step 4: Start Celery Worker (Terminal 3, Optional)
```bash
cd /Users/aryannn/Desktop/audio-processor/backend

# Activate environment
source venv/bin/activate

# Start worker
celery -A app.tasks.processing worker --loglevel=info
```

---

## 📋 Step-by-Step Manual Setup

For first-time setup or manual configuration:

### 1. Start Docker Services
```bash
cd /Users/aryannn/Desktop/audio-processor

# Start PostgreSQL, Redis, MinIO
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 2. Backend Setup
```bash
cd backend

# Create Python environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Start server
python -m uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Celery Worker (Optional)
```bash
cd ../backend
source venv/bin/activate
celery -A app.tasks.processing worker --loglevel=info
```

---

## 🔍 Verify Everything Works

### Test Frontend
```bash
curl http://localhost:3000
```

### Test Backend
```bash
curl http://localhost:8000/health
```

### Test API Upload
```bash
# Create a test audio file or use an existing one
curl -F "file=@test-audio.wav" http://localhost:8000/api/audio/upload
```

### Test MinIO
Open http://localhost:9001 in browser
- Username: `minioadmin`
- Password: `minioadmin`

---

## 🐳 Docker Commands Reference

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
docker-compose logs -f redis
```

### Stop Services
```bash
# Stop running services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove everything (including volumes!)
docker-compose down -v
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart frontend
```

### Execute Commands in Container
```bash
# Run bash in backend
docker-compose exec backend bash

# Run command in container
docker-compose exec backend python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### View Database
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U audiouser -d audiodb

# List tables (inside psql)
\dt
```

### Check Service Health
```bash
# Check all services
docker-compose ps

# Check specific logs for errors
docker-compose logs backend | grep -i error
```

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Find what's using port 3000
lsof -i :3000

# Find what's using port 8000
lsof -i :8000

# Kill process (replace PID with actual number)
kill -9 <PID>
```

### Database Connection Error
```bash
# Restart database service
docker-compose restart postgres

# Check database logs
docker-compose logs postgres

# Verify database is running
docker-compose exec postgres pg_isready -U audiouser
```

### Frontend API Connection Error
Check that backend is running and accessible:
```bash
curl http://localhost:8000/health
```

If not working, check `.env.local` in frontend folder has:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Celery Worker Not Processing Tasks
1. Verify Redis is running: `docker-compose logs redis`
2. Check Celery logs for errors
3. Verify broker URL in .env: `CELERY_BROKER_URL`

### MinIO Connection Failed
```bash
# Check MinIO is running
docker-compose logs minio

# Check connectivity
curl http://localhost:9000/minio/health/live
```

---

## 📊 Service Status Monitoring

### Monitor All Services
```bash
# Watch service status (updates every 2 seconds)
watch docker-compose ps
```

### Check Resource Usage
```bash
# View CPU, memory usage
docker stats audio-processor-postgres audio-processor-redis audio-processor-backend
```

### View Complete Logs
```bash
# Last 100 lines of all logs
docker-compose logs --tail=100

# Follow logs in real-time
docker-compose logs -f

# Logs for specific time range
docker-compose logs --since 2024-01-15T10:00:00 --until 2024-01-15T11:00:00
```

---

## 🧹 Cleanup

### Remove Stopped Containers
```bash
docker-compose down
```

### Remove All Data (⚠️ Destructive)
```bash
# Remove containers and volumes (database/storage deleted)
docker-compose down -v
```

### Clean Up Docker System
```bash
# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything unused (be careful!)
docker system prune -a
```

---

## 📝 Environment Variables

If you need to customize, edit `.env` file:

```bash
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=audiouser
POSTGRES_PASSWORD=audiopass
POSTGRES_DB=audiodb

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=redispass

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_HOST=localhost
MINIO_PORT=9000
AWS_S3_BUCKET=audio-processor

# Backend
BACKEND_SECRET_KEY=your-secret-key-change-in-production
BACKEND_URL=http://localhost:8000
ENV=development
DEBUG=true
```

---

## 🎯 Next Steps After Running

1. **Upload an audio file**: Go to http://localhost:3000 and upload a WAV/MP3 file
2. **Create a processing job**: Select filter type and click "Process Audio"
3. **Monitor progress**: Watch job status in real-time
4. **Check API**: Visit http://localhost:8000/docs for interactive API testing
5. **View database**: Connect to PostgreSQL to inspect data

---

## 🆘 Need Help?

1. Check logs: `docker-compose logs -f`
2. Review [SETUP.md](docs/SETUP.md) for detailed setup
3. Review [API.md](docs/API.md) for endpoint reference
4. Check [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design

---

## 📚 Development Workflow

### Code Changes

**Backend Changes:**
- Changes to Python files auto-reload with `--reload` flag
- Database schema changes require manual migration
- New dependencies need: `pip install <package>` then rebuild Docker image

**Frontend Changes:**
- Changes auto-reload in dev mode
- New dependencies need: `npm install <package>` then rebuild Docker image

### Database Migrations

For now, database schema is managed with SQLAlchemy:
```bash
cd backend
source venv/bin/activate

# Reset database (destructive!)
python -c "from app.database import Base, engine; Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)"
```

### Building Docker Images

When dependencies change:
```bash
# Rebuild backend
docker-compose build backend

# Rebuild frontend
docker-compose build frontend

# Rebuild all
docker-compose build

# Rebuild and restart
docker-compose up -d --build
```

---

**Happy audio processing! 🎵**

# 🚀 QUICK RUN COMMANDS

## Fastest Way (One Command - Full Docker Stack)
```bash
cd /Users/aryannn/Desktop/audio-processor
chmod +x docker/start-prod.sh
./docker/start-prod.sh
```
Then open: http://localhost:3000

---

## Development Mode (Recommended for Coding)

### Terminal 1: Infrastructure
```bash
cd /Users/aryannn/Desktop/audio-processor
chmod +x docker/start-dev.sh
./docker/start-dev.sh
```

### Terminal 2: Backend
```bash
cd /Users/aryannn/Desktop/audio-processor/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

### Terminal 3: Frontend
```bash
cd /Users/aryannn/Desktop/audio-processor/frontend
npm install
npm run dev
```

### Terminal 4: Celery (Optional)
```bash
cd /Users/aryannn/Desktop/audio-processor/backend
source venv/bin/activate
celery -A app.tasks.processing worker --loglevel=info
```

---

## Access Points
| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| MinIO Console | http://localhost:9001 |

---

## First Time Setup (If Not Using Docker)
```bash
# 1. Start services
cd /Users/aryannn/Desktop/audio-processor
docker-compose up -d

# 2. Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload

# 3. Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## Stop Everything
```bash
docker-compose down
```

---

## View Logs
```bash
docker-compose logs -f [service-name]
```

---

## More Details
See [RUN.md](RUN.md) for complete guide

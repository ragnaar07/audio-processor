#!/bin/bash

# Start Development Services Only (PostgreSQL, Redis, MinIO)
echo "🐳 Starting Docker services (PostgreSQL, Redis, MinIO)..."
cd "$(dirname "$0")/.."
docker-compose up -d

echo "✅ Services started!"
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "📍 Access Points:"
echo "  - PostgreSQL: localhost:5432 (user: audiouser, pass: audiopass)"
echo "  - Redis: localhost:6379 (password: redispass)"
echo "  - MinIO API: localhost:9000 (user: minioadmin, pass: minioadmin)"
echo "  - MinIO Console: http://localhost:9001"
echo ""
echo "💡 Next, start the application servers in separate terminals:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend && source venv/bin/activate && python -m uvicorn main:app --reload"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend && npm run dev"
echo ""
echo "Terminal 3 - Celery Worker (optional):"
echo "  cd backend && source venv/bin/activate && celery -A app.tasks.processing worker --loglevel=info"

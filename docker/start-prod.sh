#!/bin/bash

# Start All Services (Production-like setup with Docker)
echo "🎵 Starting complete audio processor stack..."
cd "$(dirname "$0")/.."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
fi

# Determine compose command
if command -v docker-compose >/dev/null 2>&1; then
    COMPOSE_CMD="docker-compose"
elif docker compose version >/dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ Docker Compose is not installed. Please install docker-compose or the Docker Compose plugin."
    exit 1
fi

echo "🐳 Building and starting Docker containers..."
$COMPOSE_CMD -f docker-compose.yml -f docker/docker-compose.prod.yml up -d
if [ $? -ne 0 ]; then
    echo "❌ Failed to start containers. Check Docker daemon and compose configuration."
    exit 1
fi

echo "✅ All services are starting!"
echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

echo "📊 Service Status:"
$COMPOSE_CMD -f docker-compose.yml -f docker/docker-compose.prod.yml ps

echo ""
echo "📍 Access Points:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - MinIO Console: http://localhost:9001 (minioadmin/minioadmin)"
echo ""
echo "📋 Useful commands:"
echo "  - View logs: $COMPOSE_CMD -f docker-compose.yml -f docker/docker-compose.prod.yml logs -f [service-name]"
echo "  - Stop services: $COMPOSE_CMD -f docker-compose.yml -f docker/docker-compose.prod.yml down"
echo "  - Restart service: $COMPOSE_CMD -f docker-compose.yml -f docker/docker-compose.prod.yml restart [service-name]"
echo "  - Interactive bash: $COMPOSE_CMD -f docker-compose.yml -f docker/docker-compose.prod.yml exec [service-name] sh"
echo ""

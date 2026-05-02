# Deployment

## Docker Compose

The production-like Docker stack builds and runs PostgreSQL, Redis, MinIO, FastAPI, Celery, and Next.js:

```bash
./docker/start-prod.sh
```

Access points:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs
- MinIO console: http://localhost:9001

## Required Environment

Copy `.env.example` to `.env` and replace all development secrets before deploying to a shared or public environment.

Important variables:

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- `REDIS_PASSWORD`
- `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_BUCKET`
- `BACKEND_SECRET_KEY`
- `NEXT_PUBLIC_API_URL`

## Production Notes

- The compose production override runs built images without source bind mounts or hot reload commands.
- The backend creates the configured MinIO bucket on startup when MinIO is reachable.
- Uploaded and processed files are stored in MinIO for the Docker stack, so the API and Celery worker share the same storage.
- For public deployments, put the backend behind HTTPS and set `NEXT_PUBLIC_API_URL` to that public backend URL before building the frontend image.

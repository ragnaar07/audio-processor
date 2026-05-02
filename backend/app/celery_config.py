"""
Celery configuration and task definitions.

This module configures Celery for distributed task processing.
"""

from celery import Celery, Task
from celery.schedules import crontab
from app.config import get_settings

settings = get_settings()

# Create Celery app instance
celery_app = Celery(
    "audio_processor",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Configure Celery
celery_app.conf.update(
    # Serialization
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # Timezone
    timezone='UTC',
    enable_utc=True,
    
    # Task settings
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    
    # Worker settings
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    
    # Result backend
    result_expires=3600,  # 1 hour
    
    # Routing
    task_default_queue='default',
    task_queues={
        'default': {'exchange': 'tasks', 'routing_key': 'task.#'},
        'processing': {'exchange': 'processing', 'routing_key': 'process.#'},
    },
)

# Optional: Configure periodic tasks
celery_app.conf.beat_schedule = {
    'cleanup-old-jobs': {
        'task': 'app.tasks.cleanup.cleanup_old_jobs',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
}


# Custom task base class for error handling
class CallbackTask(Task):
    """Task with error callback."""
    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print(f'Task {task_id} retrying: {exc}')
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f'Task {task_id} failed: {exc}')
    
    def on_success(self, result, task_id, args, kwargs):
        print(f'Task {task_id} succeeded: {result}')


celery_app.Task = CallbackTask

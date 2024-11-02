from config.env import env

# Use Redis as the broker
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = "django-db"


CELERY_TIMEZONE = "UTC"
CELERY_TASK_SOFT_TIME_LIMIT = 20  
CELERY_TASK_TIME_LIMIT = 30  
CELERY_TASK_MAX_RETRIES = 3

import redis
from rq import Queue
from config import settings

# Redis connection
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

# RQ Queue for image processing
image_processing_queue = Queue(settings.RQ_QUEUE_NAME, connection=redis_client)

def get_redis_client():
    """Get Redis client instance."""
    return redis_client

def get_image_processing_queue():
    """Get RQ queue for image processing."""
    return image_processing_queue

def test_redis_connection():
    """Test Redis connection."""
    try:
        redis_client.ping()
        return True
    except redis.ConnectionError:
        return False

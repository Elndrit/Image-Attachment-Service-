import redis
from rq import Queue
from config import REDIS_URL, RQ_QUEUE_NAME

# Redis connection
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# RQ Queue for image processing
image_processing_queue = Queue(RQ_QUEUE_NAME, connection=redis_client)

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

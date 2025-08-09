#!/usr/bin/env python3
"""
Script to start the RQ worker for background image processing
"""

import os
import sys
from rq import Worker, Queue, Connection
from redis import Redis
from config import settings

def start_worker():
    """Start the RQ worker for image processing."""
    print("🚀 Starting RQ Worker for Image Processing...")
    print(f"📡 Connecting to Redis at {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    print(f"📋 Queue: {settings.RQ_QUEUE_NAME}")
    
    # Create Redis connection
    redis_conn = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )
    
    # Create queue
    queue = Queue(settings.RQ_QUEUE_NAME, connection=redis_conn)
    
    # Start worker
    with Connection(redis_conn):
        worker = Worker([queue], name='image_processing_worker')
        print("✅ Worker started successfully!")
        print("⏳ Waiting for jobs...")
        worker.work()

if __name__ == "__main__":
    try:
        start_worker()
    except KeyboardInterrupt:
        print("\n🛑 Worker stopped by user")
    except Exception as e:
        print(f"❌ Error starting worker: {e}")
        sys.exit(1)

#!/usr/bin/env python3
"""
Test script to verify Redis connection and RQ setup
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.redis_client import test_redis_connection, get_image_processing_queue
from app.worker import queue_image_processing, get_job_status
from config import settings

def test_redis_connection():
    """Test Redis connection."""
    print("🔍 Testing Redis connection...")
    
    try:
        is_connected = test_redis_connection()
        if is_connected:
            print("✅ Redis connection successful!")
            return True
        else:
            print("❌ Redis connection failed!")
            return False
    except Exception as e:
        print(f"❌ Redis connection error: {e}")
        return False

def test_rq_queue():
    """Test RQ queue functionality."""
    print("\n🔍 Testing RQ queue...")
    
    try:
        queue = get_image_processing_queue()
        print(f"✅ RQ queue '{settings.RQ_QUEUE_NAME}' created successfully!")
        
        # Test job creation
        test_data = {
            'file_path': '/tmp/test.jpg',
            'filename': 'test.jpg',
            'user_id': 1,
            'description': 'Test job'
        }
        
        job_id = queue_image_processing(test_data)
        print(f"✅ Test job created with ID: {job_id}")
        
        # Test job status
        status = get_job_status(job_id)
        print(f"✅ Job status retrieved: {status['status']}")
        
        return True
    except Exception as e:
        print(f"❌ RQ queue error: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Testing Redis and RQ Setup")
    print("=" * 50)
    
    # Test Redis connection
    redis_ok = test_redis_connection()
    
    if not redis_ok:
        print("\n❌ Redis connection failed. Please make sure Redis is running:")
        print("   - Start Redis server: redis-server")
        print("   - Or use Docker: docker run -d -p 6379:6379 redis:alpine")
        return False
    
    # Test RQ queue
    rq_ok = test_rq_queue()
    
    if rq_ok:
        print("\n🎉 All tests passed! Redis and RQ are working correctly.")
        print("\nNext steps:")
        print("1. Start the FastAPI server: python -m uvicorn app.main:app --reload")
        print("2. Start the RQ worker: python start_worker.py")
        return True
    else:
        print("\n❌ RQ tests failed. Please check the configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

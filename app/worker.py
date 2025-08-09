# Redis Consumer for EAN code processing
# This file contains the background worker logic for processing EAN codes and fetching images

import os
import uuid
import requests
from PIL import Image
from typing import Dict, Any
from rq import get_current_job
from .redis_client import get_redis_client, get_image_processing_queue
from config import settings

def process_ean_task(ean_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Background task for processing EAN codes and fetching images.
    
    Args:
        ean_data: Dictionary containing EAN information
            - ean_code: The EAN code to process
            - user_id: ID of the user who requested the image
            - description: Optional description
    
    Returns:
        Dict containing processing results
    """
    job = get_current_job()
    
    try:
        # Extract EAN data
        ean_code = ean_data.get('ean_code')
        user_id = ean_data.get('user_id')
        description = ean_data.get('description', '')
        
        if not ean_code:
            raise ValueError("EAN code is required")
        
        # Fetch image from external API
        image_info = _fetch_image_from_external_api(ean_code)
        
        # Save the image locally
        saved_info = _save_ean_image(ean_code, image_info)
        
        # Update job status
        job.meta['status'] = 'completed'
        job.meta['image_info'] = saved_info
        job.save_meta()
        
        return {
            'status': 'success',
            'message': 'EAN image fetched and saved successfully',
            'ean_code': ean_code,
            'image_info': saved_info,
            'user_id': user_id,
            'description': description
        }
        
    except Exception as e:
        # Update job status with error
        job.meta['status'] = 'failed'
        job.meta['error'] = str(e)
        job.save_meta()
        
        return {
            'status': 'error',
            'message': f'EAN processing failed: {str(e)}',
            'error': str(e)
        }

def _fetch_image_from_external_api(ean_code: str) -> Dict[str, Any]:
    """
    Fetch image from external API using EAN code.
    
    Args:
        ean_code: The EAN code to search for
    
    Returns:
        Dict containing image information from external API
    """
    # TODO: Replace with actual external API endpoint
    # This is a placeholder for the external API call
    
    # Example external API call:
    # api_url = f"https://external-api.com/products/{ean_code}/image"
    # headers = {"Authorization": f"Bearer {settings.EXTERNAL_API_KEY}"}
    # response = requests.get(api_url, headers=headers)
    
    # For now, return mock data
    return {
        'image_url': f"https://example.com/images/{ean_code}.jpg",
        'product_name': f"Product {ean_code}",
        'image_format': 'jpeg',
        'image_size': (800, 600)
    }

def _save_ean_image(ean_code: str, image_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Download and save image for EAN code.
    
    Args:
        ean_code: The EAN code
        image_info: Image information from external API
    
    Returns:
        Dict containing saved image information
    """
    # Create upload directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Generate filename based on EAN code
    filename = f"{ean_code}.jpg"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    try:
        # Download image from external API
        # TODO: Replace with actual image download
        # response = requests.get(image_info['image_url'])
        # with open(file_path, 'wb') as f:
        #     f.write(response.content)
        
        # For now, create a placeholder image
        img = Image.new('RGB', (800, 600), color='lightblue')
        img.save(file_path, 'JPEG')
        
        return {
            'ean_code': ean_code,
            'filename': filename,
            'file_path': file_path,
            'file_size': os.path.getsize(file_path),
            'mime_type': 'image/jpeg',
            'product_name': image_info.get('product_name', ''),
            'image_url': image_info.get('image_url', '')
        }
        
    except Exception as e:
        raise Exception(f"Failed to save image for EAN {ean_code}: {str(e)}")

def queue_ean_processing(ean_data: Dict[str, Any]) -> str:
    """
    Queue an EAN code for processing.
    
    Args:
        ean_data: Dictionary containing EAN information
    
    Returns:
        Job ID for tracking
    """
    queue = get_image_processing_queue()
    job = queue.enqueue(
        process_ean_task,
        args=(ean_data,),
        job_timeout='10m',
        result_ttl=3600  # Keep results for 1 hour
    )
    return job.id

def get_job_status(job_id: str) -> Dict[str, Any]:
    """
    Get the status of a processing job.
    
    Args:
        job_id: RQ job ID
    
    Returns:
        Dict containing job status and results
    """
    queue = get_image_processing_queue()
    job = queue.fetch_job(job_id)
    
    if not job:
        return {'status': 'not_found', 'message': 'Job not found'}
    
    if job.is_finished:
        return {
            'status': 'completed',
            'result': job.result,
            'meta': job.meta
        }
    elif job.is_failed:
        return {
            'status': 'failed',
            'error': str(job.exc_info),
            'meta': job.meta
        }
    else:
        return {
            'status': 'in_progress',
            'meta': job.meta
        }

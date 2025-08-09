# API endpoints for EAN code processing and image fetching
# This file contains the main API routes for EAN processing

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from pydantic import BaseModel

from database import get_db
from models import User
from auth import get_current_active_user
from .worker import queue_ean_processing, get_job_status
from .redis_client import get_image_processing_queue

router = APIRouter()

class EANRequest(BaseModel):
    ean_code: str
    description: str = None

class EANResponse(BaseModel):
    job_id: str
    ean_code: str
    status: str
    message: str

@router.post("/fetch-image", response_model=EANResponse)
async def fetch_image_by_ean(
    ean_request: EANRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Fetch image for a given EAN code.
    Queues the EAN processing job and returns job ID for tracking.
    """
    # Validate EAN code format (basic validation)
    if not ean_request.ean_code or len(ean_request.ean_code) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid EAN code format"
        )
    
    # Queue the EAN processing job
    job_data = {
        'ean_code': ean_request.ean_code,
        'user_id': current_user.id,
        'description': ean_request.description
    }
    
    job_id = queue_ean_processing(job_data)
    
    return EANResponse(
        job_id=job_id,
        ean_code=ean_request.ean_code,
        status="queued",
        message="EAN processing job queued successfully"
    )

@router.get("/jobs/{job_id}")
async def get_job_status_endpoint(job_id: str):
    """Get the status of a background processing job."""
    return get_job_status(job_id)

@router.get("/jobs")
async def list_jobs():
    """List all jobs in the queue."""
    queue = get_image_processing_queue()
    jobs = queue.jobs
    
    return {
        "total_jobs": len(jobs),
        "jobs": [
            {
                "id": job.id,
                "status": job.get_status(),
                "created_at": job.created_at.isoformat() if job.created_at else None
            }
            for job in jobs
        ]
    }

@router.get("/images/{ean_code}")
async def get_image_by_ean(
    ean_code: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get image information for a specific EAN code.
    Returns the stored image details if available.
    """
    # TODO: Implement database lookup for EAN images
    # This will query the database for images associated with the EAN code
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="EAN image lookup not yet implemented"
    )

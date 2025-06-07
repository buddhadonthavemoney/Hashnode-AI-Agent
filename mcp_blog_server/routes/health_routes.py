"""
Health check routes for MCP Blog Server.
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends
from ..services.hashnode_service import HashnodeService
from ..config import settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "message": "MCP Blog Server is running"
    }


@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """Detailed health check including external services."""
    hashnode_service = HashnodeService()
    
    # Check Hashnode connection
    hashnode_status = "unknown"
    hashnode_info = None
    
    try:
        hashnode_info = await hashnode_service.get_publication_info()
        hashnode_status = "connected" if hashnode_info else "error"
    except Exception:
        hashnode_status = "error"
    
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "services": {
            "hashnode": {
                "status": hashnode_status,
                "publication": hashnode_info.get("title") if hashnode_info else None
            }
        },
        "config": {
            "gemini_model": settings.gemini_model,
            "max_title_length": settings.max_title_length,
            "max_notes_length": settings.max_notes_length
        }
    } 
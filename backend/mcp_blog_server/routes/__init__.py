"""
API routes for MCP Blog Server.
"""

from .blog_routes import router as blog_router
from .health_routes import router as health_router

__all__ = [
    "blog_router",
    "health_router"
]
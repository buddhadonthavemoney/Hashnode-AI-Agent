"""
Hashnode API-related Pydantic models.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class HashnodePublishRequest(BaseModel):
    """Request model for publishing to Hashnode."""
    
    title: str = Field(..., description="Blog post title")
    content_markdown: str = Field(..., description="Blog post content in markdown")
    tags: Optional[List[str]] = Field(default=None, description="Blog post tags")
    cover_image_url: Optional[str] = Field(default=None, description="Cover image URL")
    is_featured: bool = Field(default=False, description="Whether the post is featured")


class HashnodePublishResponse(BaseModel):
    """Response model for Hashnode publishing."""
    
    success: bool = Field(..., description="Whether the publishing was successful")
    post_id: Optional[str] = Field(default=None, description="Hashnode post ID")
    post_url: Optional[str] = Field(default=None, description="Published post URL")
    message: str = Field(..., description="Response message")
    error_code: Optional[str] = Field(default=None, description="Error code if failed")


class HashnodeTag(BaseModel):
    """Hashnode tag model."""
    
    id: str = Field(..., description="Tag ID")
    name: str = Field(..., description="Tag name")
    slug: str = Field(..., description="Tag slug")


class HashnodePublication(BaseModel):
    """Hashnode publication model."""
    
    id: str = Field(..., description="Publication ID")
    title: str = Field(..., description="Publication title")
    url: str = Field(..., description="Publication URL") 
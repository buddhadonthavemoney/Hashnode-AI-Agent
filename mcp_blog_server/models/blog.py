"""
Blog-related Pydantic models.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class BlogRequest(BaseModel):
    """Request model for blog generation."""
    
    title: str = Field(..., min_length=1, max_length=200, description="Blog post title")
    notes: str = Field(..., min_length=1, max_length=5000, description="Rough notes for the blog post")
    tags: Optional[List[str]] = Field(default=None, description="Optional tags for the blog post")
    publish_immediately: bool = Field(default=False, description="Whether to publish immediately to Hashnode")
    
    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
    
    @validator('notes')
    def validate_notes(cls, v):
        if not v.strip():
            raise ValueError('Notes cannot be empty')
        return v.strip()
    
    @validator('tags')
    def validate_tags(cls, v):
        if v is not None:
            return [tag.strip() for tag in v if tag.strip()]
        return v


class BlogPost(BaseModel):
    """Generated blog post model."""
    
    title: str = Field(..., description="Blog post title")
    content: str = Field(..., description="Generated markdown content")
    tags: Optional[List[str]] = Field(default=None, description="Blog post tags")
    summary: Optional[str] = Field(default=None, description="Blog post summary")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class BlogResponse(BaseModel):
    """Response model for blog generation."""
    
    success: bool = Field(..., description="Whether the generation was successful")
    blog_post: Optional[BlogPost] = Field(default=None, description="Generated blog post")
    hashnode_url: Optional[str] = Field(default=None, description="Published Hashnode URL")
    message: str = Field(..., description="Response message")
    generation_time_seconds: Optional[float] = Field(default=None, description="Time taken to generate content")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 
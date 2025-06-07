"""
Blog-related API routes for MCP Blog Server.
"""

import logging
import time
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from ..models.blog import BlogRequest, BlogResponse, BlogPost
from ..models.hashnode import HashnodePublishRequest
from ..services.gemini_service import GeminiService
from ..services.hashnode_service import HashnodeService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/blog", tags=["blog"])


@router.post("/generate", response_model=BlogResponse)
async def generate_blog_post(request: BlogRequest) -> BlogResponse:
    """
    Generate a blog post from title and notes using Gemini AI.
    
    Args:
        request: Blog generation request
        
    Returns:
        BlogResponse: Generated blog post response
    """
    start_time = time.time()
    
    try:
        logger.info(f"Generating blog post: {request.title}")
        
        # Initialize Gemini service
        gemini_service = GeminiService()
        
        # Generate blog post
        blog_post = gemini_service.generate_blog_post(
            title=request.title,
            notes=request.notes,
            tags=request.tags
        )
        
        generation_time = time.time() - start_time
        
        # If publish_immediately is True, publish to Hashnode
        hashnode_url = None
        if request.publish_immediately:
            try:
                hashnode_service = HashnodeService()
                publish_request = HashnodePublishRequest(
                    title=blog_post.title,
                    content_markdown=blog_post.content,
                    tags=blog_post.tags
                )
                
                publish_response = await hashnode_service.publish_post(publish_request)
                
                if publish_response.success:
                    hashnode_url = publish_response.post_url
                    logger.info(f"Blog post published to Hashnode: {hashnode_url}")
                else:
                    logger.warning(f"Failed to publish to Hashnode: {publish_response.message}")
                    
            except Exception as e:
                logger.error(f"Error publishing to Hashnode: {str(e)}")
                # Don't fail the entire request if publishing fails
        
        return BlogResponse(
            success=True,
            blog_post=blog_post,
            hashnode_url=hashnode_url,
            message="Blog post generated successfully" + (" and published to Hashnode" if hashnode_url else ""),
            generation_time_seconds=generation_time
        )
        
    except Exception as e:
        logger.error(f"Error generating blog post: {str(e)}")
        return BlogResponse(
            success=False,
            message=f"Failed to generate blog post: {str(e)}",
            generation_time_seconds=time.time() - start_time
        )


@router.post("/publish")
async def publish_to_hashnode(blog_post: BlogPost) -> Dict[str, Any]:
    """
    Publish an existing blog post to Hashnode.
    
    Args:
        blog_post: Blog post to publish
        
    Returns:
        Dict: Publishing response
    """
    try:
        logger.info(f"Publishing blog post to Hashnode: {blog_post.title}")
        
        hashnode_service = HashnodeService()
        
        publish_request = HashnodePublishRequest(
            title=blog_post.title,
            content_markdown=blog_post.content,
            tags=blog_post.tags
        )
        
        response = await hashnode_service.publish_post(publish_request)
        
        if response.success:
            return {
                "success": True,
                "message": response.message,
                "post_id": response.post_id,
                "post_url": response.post_url
            }
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": response.message,
                    "error_code": response.error_code
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error publishing to Hashnode: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "message": f"Publishing failed: {str(e)}",
                "error_code": "INTERNAL_ERROR"
            }
        )


@router.post("/generate-and-publish", response_model=BlogResponse)
async def generate_and_publish_blog_post(request: BlogRequest) -> BlogResponse:
    """
    Generate and immediately publish a blog post (convenience endpoint).
    
    Args:
        request: Blog generation request
        
    Returns:
        BlogResponse: Generated and published blog post response
    """
    # Force immediate publishing
    request.publish_immediately = True
    return await generate_blog_post(request)


@router.get("/publication-info")
async def get_publication_info() -> Dict[str, Any]:
    """
    Get information about the configured Hashnode publication.
    
    Returns:
        Dict: Publication information
    """
    try:
        hashnode_service = HashnodeService()
        pub_info = await hashnode_service.get_publication_info()
        
        if pub_info:
            return {
                "success": True,
                "publication": pub_info
            }
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": "Could not fetch publication information"
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching publication info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "message": f"Failed to fetch publication info: {str(e)}"
            }
        ) 
    


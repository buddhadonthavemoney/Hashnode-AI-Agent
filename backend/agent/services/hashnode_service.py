"""
Hashnode service for publishing blog posts via GraphQL API.
"""

import logging
from typing import Dict, Any, Optional

import httpx

from ..config import settings
from ..models.hashnode import HashnodePublishRequest, HashnodePublishResponse

logger = logging.getLogger(__name__)


class HashnodeService:
    """Service for publishing blog posts to Hashnode."""
    
    def __init__(self):
        """Initialize the Hashnode service."""
        self.api_url = settings.hashnode_api_url
        self.token = settings.hashnode_token
        self.publication_id = settings.hashnode_publication_id
        
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    async def publish_post(self, request: HashnodePublishRequest) -> HashnodePublishResponse:
        """
        Publish a blog post to Hashnode.
        
        Args:
            request: The publish request containing post data
            
        Returns:
            HashnodePublishResponse: Response from Hashnode API
        """
        try:
            logger.info(f"Publishing post to Hashnode: {request.title}")
            
            # Prepare the GraphQL mutation
            mutation = self._build_publish_mutation(request)
            
            # Make the API request
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    json={"query": mutation},
                    headers=self.headers,
                    timeout=30.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                # Check for GraphQL errors
                if "errors" in data:
                    error_msg = "; ".join([error["message"] for error in data["errors"]])
                    logger.error(f"GraphQL errors: {error_msg}")
                    return HashnodePublishResponse(
                        success=False,
                        message=f"GraphQL errors: {error_msg}",
                        error_code="GRAPHQL_ERROR"
                    )
                
                # Parse successful response
                post_data = data.get("data", {}).get("publishPost", {})
                
                if not post_data:
                    return HashnodePublishResponse(
                        success=False,
                        message="No post data in response",
                        error_code="EMPTY_RESPONSE"
                    )
                
                post_id = post_data.get("post", {}).get("id")
                post_url = post_data.get("post", {}).get("url")
                
                logger.info(f"Post published successfully: {post_url}")
                
                return HashnodePublishResponse(
                    success=True,
                    post_id=post_id,
                    post_url=post_url,
                    message="Post published successfully"
                )
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error publishing to Hashnode: {e}")
            return HashnodePublishResponse(
                success=False,
                message=f"HTTP error: {e.response.status_code} - {e.response.text}",
                error_code="HTTP_ERROR"
            )
        except Exception as e:
            logger.error(f"Error publishing to Hashnode: {str(e)}")
            return HashnodePublishResponse(
                success=False,
                message=f"Publishing failed: {str(e)}",
                error_code="UNKNOWN_ERROR"
            )
    
    def _build_publish_mutation(self, request: HashnodePublishRequest) -> str:
        """Build the GraphQL mutation for publishing a post."""
        
        # Prepare tags
        tags_str = ""
        if request.tags:
            # Convert tags to GraphQL array format with both name and slug
            tag_objects = []
            for tag in request.tags:
                slug = self._create_tag_slug(tag)
                tag_objects.append(f'{{name: "{self._escape_string(tag)}", slug: "{slug}"}}')
            tags_str = f"tags: [{', '.join(tag_objects)}]"
        
        # Prepare cover image
        cover_image_str = ""
        if request.cover_image_url:
            cover_image_str = f'coverImageOptions: {{coverImageURL: "{request.cover_image_url}"}}'
        
        mutation = f"""
        mutation PublishPost {{
            publishPost(input: {{
                title: "{self._escape_string(request.title)}"
                contentMarkdown: "{self._escape_string(request.content_markdown)}"
                publicationId: "{self.publication_id}"
                {tags_str}
                {cover_image_str}
                settings: {{
                    delisted: false
                    enableTableOfContent: true
                    isNewsletterActivated: false
                }}
            }}) {{
                post {{
                    id
                    title
                    url
                    slug
                    publishedAt
                }}
            }}
        }}
        """
        
        return mutation.strip()
    
    def _create_tag_slug(self, tag_name: str) -> str:
        """Create a URL-friendly slug from a tag name."""
        import re
        # Convert to lowercase, replace spaces and special chars with hyphens
        slug = re.sub(r'[^\w\s-]', '', tag_name.lower())
        slug = re.sub(r'[\s_-]+', '-', slug)
        slug = slug.strip('-')
        return slug
    
    def _escape_string(self, text: str) -> str:
        """Escape special characters for GraphQL strings."""
        # Escape quotes and backslashes
        return text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
    
    async def get_publication_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the configured publication.
        
        Returns:
            Dict containing publication info or None if error
        """
        try:
            query = f"""
            query GetPublication {{
                publication(id: "{self.publication_id}") {{
                    id
                    title
                    displayTitle
                    url
                    metaDescription
                    favicon
                    isTeam
                    followersCount
                    author {{
                        name
                        username
                    }}
                }}
            }}
            """
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    json={"query": query},
                    headers=self.headers,
                    timeout=30.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                if "errors" in data:
                    logger.error(f"Error fetching publication info: {data['errors']}")
                    return None
                
                return data.get("data", {}).get("publication")
                
        except Exception as e:
            logger.error(f"Error fetching publication info: {str(e)}")
            return None 
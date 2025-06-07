"""
Configuration management for MCP Blog Server.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Server settings
    app_name: str = "MCP Blog Server"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Gemini API settings
    gemini_api_key: str = Field(..., description="Google Gemini API key")
    gemini_model: str = "gemini-2.0-flash"
    
    # Hashnode API settings
    hashnode_api_url: str = "https://gql.hashnode.com/"
    hashnode_token: str = Field(..., description="Hashnode API token")
    hashnode_publication_id: str = Field(..., description="Hashnode publication ID")
    
    # Blog generation settings
    max_title_length: int = 200
    max_notes_length: int = 5000
    generation_timeout: int = 30


# Global settings instance
settings = Settings() 
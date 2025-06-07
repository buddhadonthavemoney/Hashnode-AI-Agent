#!/usr/bin/env python3
"""
Simple test script to verify the MCP Blog Server setup.
"""

import os
import sys

# Set mock environment variables for testing
os.environ['GEMINI_API_KEY'] = 'test_gemini_key'
os.environ['HASHNODE_TOKEN'] = 'test_hashnode_token'
os.environ['HASHNODE_PUBLICATION_ID'] = 'test_publication_id'

try:
    # Test imports
    print("Testing imports...")
    from mcp_blog_server.config import settings
    print(f"✅ Config loaded: {settings.app_name} v{settings.app_version}")
    
    from mcp_blog_server.models.blog import BlogRequest, BlogPost, BlogResponse
    print("✅ Blog models imported successfully")
    
    from mcp_blog_server.models.hashnode import HashnodePublishRequest, HashnodePublishResponse
    print("✅ Hashnode models imported successfully")
    
    from mcp_blog_server.services.gemini_service import GeminiService
    print("✅ Gemini service imported successfully")
    
    from mcp_blog_server.services.hashnode_service import HashnodeService
    print("✅ Hashnode service imported successfully")
    
    from mcp_blog_server.routes.blog_routes import router as blog_router
    from mcp_blog_server.routes.health_routes import router as health_router
    print("✅ Routes imported successfully")
    
    # Test main app
    from main import app
    print("✅ Main FastAPI app imported successfully")
    
    print("\n🎉 All tests passed! The MCP Blog Server is ready to use.")
    print("\nNext steps:")
    print("1. Copy .env.example to .env")
    print("2. Add your real API keys to .env")
    print("3. Run: python main.py")
    print("4. Visit: http://localhost:8000/docs")
    
except Exception as e:
    print(f"❌ Test failed: {str(e)}")
    sys.exit(1) 
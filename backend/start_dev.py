#!/usr/bin/env python3
"""
Development startup script for MCP Blog Server.
Sets environment variables and starts the server.
"""

import os
import subprocess
import sys

def main():
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("📋 Please create a .env file with your API keys.")
        print("💡 You can copy .env.example as a starting point:")
        print("   cp .env.example .env")
        print("   # Then edit .env with your real API keys")
        return 1
    
    # Load environment variables from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check if required variables are set
        required_vars = ['GEMINI_API_KEY', 'HASHNODE_TOKEN', 'HASHNODE_PUBLICATION_ID']
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var) or os.getenv(var) == f'your_{var.lower()}_here':
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing or invalid environment variables: {', '.join(missing_vars)}")
            print("📋 Please set these variables in your .env file with real values.")
            return 1
            
        print("✅ Environment variables loaded successfully!")
        print("🚀 Starting MCP Blog Server...")
        
        # Start the server
        subprocess.run([sys.executable, 'main.py'])
        
    except ImportError:
        print("❌ python-dotenv not installed. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'python-dotenv'])
        print("✅ python-dotenv installed. Please run this script again.")
        return 1
    except Exception as e:
        print(f"❌ Error starting server: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main()) 
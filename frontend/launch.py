#!/usr/bin/env python3
"""
Simple launcher for the MCP Blog Server Frontend.
This script starts a local HTTP server to serve the frontend files.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# Configuration
PORT = 3003
HOST = "0.0.0.0"  # Listen on all interfaces for Docker

def main():
    """Launch the frontend with a local HTTP server."""
    
    # Get the directory where this script is located
    frontend_dir = Path(__file__).parent
    
    # Change to the frontend directory
    os.chdir(frontend_dir)
    
    # Create HTTP server
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer((HOST, PORT), handler) as httpd:
            url = f"http://{HOST}:{PORT}"
            
            print("🚀 MCP Blog Server Frontend")
            print("=" * 40)
            print(f"📡 Server running at: {url}")
            print(f"📁 Serving files from: {frontend_dir}")
            print("\n💡 Make sure the MCP Blog Server is running on http://localhost:8000")
            
            # Only open browser if not in Docker (when HOST is localhost)
            if HOST == "localhost":
                print("\n🌐 Opening browser...")
                webbrowser.open(url)
            
            print(f"\n✅ Frontend launched successfully!")
            print("⏹️  Press Ctrl+C to stop the server\n")
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("👋 Goodbye!")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Error: Port {PORT} is already in use")
            print(f"💡 Try using a different port or stop the process using port {PORT}")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
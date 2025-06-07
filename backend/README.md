# MCP Blog Server

A modular FastAPI application that generates and publishes blog posts using Google Gemini AI and Hashnode's GraphQL API.

## Features

- 🤖 **AI-Powered Content Generation**: Uses Google Gemini to transform rough notes into polished blog posts
- 📝 **Markdown Output**: Generates properly formatted Markdown content
- 🚀 **Auto Publishing**: Direct integration with Hashnode for seamless publishing
- 🔧 **Modular Architecture**: Clean separation of concerns with services, models, and routes
- ⚡ **Fast API**: Built on FastAPI for high performance and automatic API documentation
- 🌐 **RESTful API**: Easy-to-use REST endpoints for all operations
- 😄 **Personality**: Captures your unique voice and tone (including humor and personality)

## Project Structure

```
mcp_blog_server/
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── test_server.py            # Test script to verify setup
├── start_dev.py              # Development startup script
├── mcp_blog_server/
│   ├── __init__.py
│   ├── config.py             # Configuration management
│   ├── models/               # Pydantic data models
│   │   ├── blog.py          # Blog-related models
│   │   └── hashnode.py      # Hashnode API models
│   ├── services/            # Business logic
│   │   ├── gemini_service.py    # AI content generation
│   │   └── hashnode_service.py  # Hashnode publishing
│   └── routes/              # API endpoints
│       ├── blog_routes.py   # Blog operations
│       └── health_routes.py # Health checks
```

## Quick Start

### 1. Clone and Setup

```bash
git clone <repo-url>
cd mcp_blog_server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your API credentials:

```env
# Required API Keys
GEMINI_API_KEY=your_actual_gemini_api_key_here
HASHNODE_TOKEN=your_actual_hashnode_token_here
HASHNODE_PUBLICATION_ID=your_actual_publication_id_here

# Optional Settings
DEBUG=false
HOST=0.0.0.0
PORT=8000
GEMINI_MODEL=gemini-pro
```

### 3. Test the Setup

```bash
python test_server.py
```

### 4. Start the Server

Option A - Using the development script (recommended):
```bash
python start_dev.py
```

Option B - Direct startup:
```bash
python main.py
```

Option C - Using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Root Endpoint**: http://localhost:8000/

## API Endpoints

### Blog Operations

#### `POST /blog/generate`
Generate a blog post from title and notes.

**Request Body:**
```json
{
  "title": "Getting Started with FastAPI",
  "notes": "FastAPI is a modern Python web framework. Key features include automatic API docs, type hints, async support.",
  "tags": ["python", "fastapi", "web-development"],
  "publish_immediately": false
}
```

**Response:**
```json
{
  "success": true,
  "blog_post": {
    "title": "Getting Started with FastAPI",
    "content": "# Getting Started with FastAPI\n\n...",
    "tags": ["python", "fastapi", "web-development"],
    "summary": "FastAPI is a modern Python web framework...",
    "created_at": "2024-01-01T12:00:00"
  },
  "hashnode_url": null,
  "message": "Blog post generated successfully",
  "generation_time_seconds": 3.45
}
```

#### `POST /blog/publish`
Publish an existing blog post to Hashnode.

**Request Body:**
```json
{
  "title": "My Blog Post",
  "content": "# My Blog Post\n\nContent here...",
  "tags": ["example"],
  "summary": "A sample blog post",
  "created_at": "2024-01-01T12:00:00"
}
```

#### `POST /blog/generate-and-publish`
Generate and immediately publish a blog post (convenience endpoint).

#### `GET /blog/publication-info`
Get information about the configured Hashnode publication.

### Health Checks

#### `GET /health`
Basic health check endpoint.

#### `GET /health/detailed`
Detailed health check including external service status.

## Usage Examples

### Generate a Blog Post

```bash
curl -X POST "http://localhost:8000/blog/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Advanced Python Tips",
    "notes": "List comprehensions, decorators, context managers, async/await patterns. Make it funny and engaging.",
    "tags": ["python", "tips", "advanced"],
    "publish_immediately": false
  }'
```

### Generate and Publish Immediately

```bash
curl -X POST "http://localhost:8000/blog/generate-and-publish" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Why I Love Bug Hunting",
    "notes": "Debugging is like being a detective. Sometimes the bug is obvious, sometimes it hides. Add some humor about common debugging experiences.",
    "tags": ["debugging", "programming", "humor"]
  }'
```

### Check Publication Info

```bash
curl -X GET "http://localhost:8000/blog/publication-info"
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `HASHNODE_TOKEN` | Hashnode API token | Yes | - |
| `HASHNODE_PUBLICATION_ID` | Your Hashnode publication ID | Yes | - |
| `DEBUG` | Enable debug mode | No | `false` |
| `HOST` | Server host | No | `0.0.0.0` |
| `PORT` | Server port | No | `8000` |
| `GEMINI_MODEL` | Gemini model to use | No | `gemini-pro` |
| `MAX_TITLE_LENGTH` | Maximum title length | No | `200` |
| `MAX_NOTES_LENGTH` | Maximum notes length | No | `5000` |
| `GENERATION_TIMEOUT` | Generation timeout (seconds) | No | `30` |

### Getting API Keys

#### Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

#### Hashnode Token
1. Go to [Hashnode Settings → Developer](https://hashnode.com/settings/developer)
2. Generate a new Personal Access Token
3. Copy the token to your `.env` file

#### Publication ID
1. Visit your Hashnode publication dashboard
2. Go to Publication Settings
3. Find your publication ID in the URL or settings
4. Copy the ID to your `.env` file

## Development

### Running Tests

```bash
python test_server.py
```

### Development Mode

For development with auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Project Architecture

The application follows a clean architecture pattern:

- **`main.py`**: FastAPI application setup and configuration
- **`config.py`**: Centralized configuration management using Pydantic Settings
- **`models/`**: Pydantic models for request/response validation
- **`services/`**: Business logic for AI generation and Hashnode publishing
- **`routes/`**: API endpoint definitions

### Adding New Features

1. **New Models**: Add to `models/` directory
2. **New Services**: Add to `services/` directory
3. **New Routes**: Add to `routes/` directory and include in `main.py`
4. **Configuration**: Add new settings to `config.py`

## Troubleshooting

### Common Issues

1. **Environment Variables Not Set**
   - Error: `ValidationError: Field required`
   - Solution: Ensure all required variables are set in `.env`

2. **API Key Invalid**
   - Error: `Authentication failed`
   - Solution: Verify your API keys are correct and active

3. **Port Already in Use**
   - Error: `Address already in use`
   - Solution: Change the port in `.env` or kill the process using the port

4. **Import Errors**
   - Error: `ModuleNotFoundError`
   - Solution: Ensure virtual environment is activated and dependencies installed

### Getting Help

- Check the interactive API docs at `/docs`
- Use the health endpoints to verify service status
- Run the test script to validate setup

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if needed
5. Submit a pull request

## License

MIT License - feel free to use this project as you wish!

## Changelog

### v1.0.0
- Initial release
- Gemini AI integration for blog generation
- Hashnode publishing support
- Clean modular architecture
- Comprehensive API documentation
- Health check endpoints
- Environment-based configuration 
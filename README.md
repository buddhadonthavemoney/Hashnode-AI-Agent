# Hashnode AI agent

A modular FastAPI application that receives blog titles and rough notes, uses Gemini AI to convert them into Markdown blog posts, and publishes them to Hashnode using GraphQL API.

## 🚀 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- Gemini API key
- Hashnode API token and publication ID

### Setup

1. **Clone and configure environment:**
   ```bash
   git clone https://github.com/buddhadonthavemoney/Hashnode-AI-Agent
   
   # Copy environment template
   cp backend/.env.example backend/.env
   
   # Edit backend/.env with your API keys:
   # GEMINI_API_KEY=your_gemini_api_key
   # HASHNODE_TOKEN=your_hashnode_token
   # HASHNODE_PUBLICATION_ID=your_publication_id
   ```

2. **Start the application:**
   ```bash
   docker-compose up
   ```

3. **Access the application:**
   - Frontend: http://localhost:3003
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🏗️ Architecture

```
├── backend/                 # FastAPI backend
│   ├── agent/    # Application package
│   │   ├── config.py       # Configuration management
│   │   ├── models/         # Pydantic models
│   │   ├── services/       # Business logic
│   │   └── routes/         # API endpoints
│   ├── main.py             # Application entry point
│   ├── start_dev.py        # Development server
│   └── Dockerfile          # Backend container
├── frontend/               # Web frontend
│   ├── index.html          # Main HTML
│   ├── styles.css          # Styling
│   ├── script.js           # JavaScript functionality
│   ├── launch.py           # Frontend server
│   └── Dockerfile          # Frontend container
└── docker-compose.yml      # Container orchestration
```

## ✨ Features

### Backend
- **🤖 AI Content Generation**: Uses Google Gemini to create engaging blog posts
- **📝 Markdown Output**: Generates clean, properly formatted markdown
- **🚀 Hashnode Publishing**: Direct integration with Hashnode GraphQL API
- **🏷️ Tag Management**: Automatic tag slug generation and validation
- **📊 Health Monitoring**: Built-in health checks and status endpoints
- **🔧 Modular Design**: Clean separation of concerns

### Frontend
- **📱 Responsive Design**: Works on desktop and mobile
- **🎨 Modern UI**: Clean, professional interface
- **⚡ Real-time Status**: Live server status monitoring
- **🔄 Tab Navigation**: Easy switching between functions
- **📋 Content Preview**: Markdown rendering with syntax highlighting
- **🔗 One-click Copy**: Transfer generated content to publish form

## 🛠️ Development

### Local Development (without Docker)

1. **Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   python start_dev.py
   ```

2. **Frontend:**
   ```bash
   cd frontend
   python launch.py
   ```

### API Endpoints

- `POST /blog/generate` - Generate blog post from notes
- `POST /blog/publish` - Publish blog post to Hashnode
- `POST /blog/generate-and-publish` - One-step generation and publishing
- `GET /blog/publication-info` - Get Hashnode publication details
- `GET /health` - Health check
- `GET /health/detailed` - Detailed service status

### Environment Variables

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here
HASHNODE_TOKEN=your_hashnode_token_here
HASHNODE_PUBLICATION_ID=your_publication_id_here

# Optional
DEBUG=True
LOG_LEVEL=INFO
GEMINI_MODEL=gemini-2.0-flash
HASHNODE_API_URL=https://gql.hashnode.com/
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

## 🔧 Configuration

### Gemini AI Setup
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `backend/.env` as `GEMINI_API_KEY`

### Hashnode Setup
1. Get your API token from [Hashnode](https://hashnode.com/settings/developer)
2. Find your publication ID from your blog's settings
3. Add both to `backend/.env`

## 📦 Docker Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🩺 Health Checks

Both services include health checks:
- Backend: `curl http://localhost:8000/health`
- Frontend: `curl http://localhost:3003/`

## 🐛 Troubleshooting

### Common Issues

1. **Port conflicts:**
   ```bash
   # Change ports in docker-compose.yml
   ports:
     - "8001:8000"  # Use different host port
   ```

2. **Environment variables not loaded:**
   ```bash
   # Ensure backend/.env exists with proper values
   cat backend/.env
   ```

3. **Container build issues:**
   ```bash
   # Clean rebuild
   docker-compose down
   docker-compose build --no-cache
   docker-compose up
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google Gemini AI for content generation
- Hashnode for the publishing platform
- FastAPI for the excellent web framework 
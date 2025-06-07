# MCP Blog Server Frontend

A minimal and attractive web interface for the MCP Blog Server that provides AI-powered blog generation and publishing to Hashnode.

## Features

- **📝 Generate Blog Posts**: Create content from title and rough notes using AI
- **🚀 Publish to Hashnode**: Publish markdown content directly to your Hashnode blog
- **⚡ One-Click Workflow**: Generate and publish in a single operation
- **📱 Responsive Design**: Works perfectly on desktop and mobile devices
- **🎨 Modern UI**: Clean, professional interface with smooth animations
- **📊 Real-time Status**: Live server status monitoring

## Quick Start

1. **Start the MCP Blog Server** (from the project root):
   ```bash
   python main.py
   ```

2. **Open the frontend** in your browser:
   ```bash
   # Navigate to the frontend directory
   cd frontend
   
   # Open index.html in your browser
   open index.html  # macOS
   # or
   xdg-open index.html  # Linux
   # or simply open frontend/index.html in your browser
   ```

3. **Configure your environment** (if not already done):
   - Ensure your `.env` file has the required API keys
   - Make sure the MCP Blog Server is running on `http://localhost:8000`

## Usage

### 🎯 Generate Blog Posts
1. Click on the "Generate Blog" tab
2. Enter your blog title and rough notes
3. Add tags (optional, comma-separated)
4. Click "Generate Blog Post"
5. Review the generated content
6. Use "Copy to Publish Form" to move content for publishing

### 📤 Publish Content
1. Click on the "Publish Blog" tab
2. Enter your title and markdown content
3. Add tags and cover image URL (optional)
4. Click "Publish to Hashnode"
5. View your published post via the provided link

### 🚀 Generate & Publish
1. Click on the "Generate & Publish" tab
2. Enter your title and rough notes
3. Add tags (optional)
4. Click "Generate & Publish"
5. The system will generate content and automatically publish it

## Features Overview

### Server Status Monitoring
- **🟢 Green**: Server is online and ready
- **🟡 Yellow**: Checking server status
- **🔴 Red**: Server is offline or has errors

### Interactive Tabs
- **Generate Blog**: AI-powered content creation
- **Publish Blog**: Direct publishing to Hashnode
- **Generate & Publish**: Complete workflow automation

### Content Preview
- Real-time markdown rendering
- Formatted display of generated content
- Easy content copying between forms

## Requirements

- MCP Blog Server running on `http://localhost:8000`
- Modern web browser with JavaScript enabled
- Internet connection for external resources (fonts, icons)

## Browser Compatibility

- ✅ Chrome/Chromium 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

## Customization

### Changing API URL
Edit the `API_BASE_URL` in `script.js`:
```javascript
const API_BASE_URL = 'http://your-server:port';
```

### Styling
Modify `styles.css` to customize:
- Color scheme
- Layout dimensions
- Animation timing
- Responsive breakpoints

## Troubleshooting

### Server Connection Issues
- Ensure MCP Blog Server is running
- Check that the API URL is correct
- Verify CORS settings allow frontend origin

### Publishing Failures
- Verify Hashnode API credentials in `.env`
- Check publication ID configuration
- Ensure content follows Hashnode's requirements

### Display Issues
- Clear browser cache
- Check browser console for JavaScript errors
- Ensure all external resources load properly

## Files Structure

```
frontend/
├── index.html      # Main HTML structure
├── styles.css      # Styling and animations
├── script.js       # JavaScript functionality
└── README.md       # This file
```

## External Dependencies

- **Inter Font**: Professional typography
- **Font Awesome**: Icons and visual elements
- **CSS Grid/Flexbox**: Modern layout systems

No build process required - just open and use! 🎉 
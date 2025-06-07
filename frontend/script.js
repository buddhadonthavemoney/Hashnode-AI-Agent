// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const statusIndicator = document.getElementById('statusIndicator');
const statusDot = statusIndicator.querySelector('.status-dot');
const statusText = statusIndicator.querySelector('.status-text');
const loadingOverlay = document.getElementById('loadingOverlay');
const loadingText = document.getElementById('loadingText');

// Store generated blog post data
let currentBlogPost = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
    initializeForms();
    checkServerStatus();
    
    // Check server status every 30 seconds
    setInterval(checkServerStatus, 30000);
});

// Tab functionality
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

// Form initialization
function initializeForms() {
    // Generate form
    const generateForm = document.getElementById('generateForm');
    generateForm.addEventListener('submit', handleGenerateSubmit);
    
    // Publish form
    const publishForm = document.getElementById('publishForm');
    publishForm.addEventListener('submit', handlePublishSubmit);
    
    // Combo form
    const comboForm = document.getElementById('comboForm');
    comboForm.addEventListener('submit', handleComboSubmit);
}

// Server status check
async function checkServerStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            updateStatus('online', 'Server Online');
        } else {
            updateStatus('offline', 'Server Error');
        }
    } catch (error) {
        updateStatus('offline', 'Server Offline');
    }
}

function updateStatus(status, text) {
    statusDot.className = `status-dot ${status}`;
    statusText.textContent = text;
}

// Loading overlay
function showLoading(text = 'Processing...') {
    loadingText.textContent = text;
    loadingOverlay.classList.add('show');
}

function hideLoading() {
    loadingOverlay.classList.remove('show');
}

// Utility functions
function parseTags(tagsString) {
    if (!tagsString) return null;
    return tagsString.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0);
}

function formatTags(tagsArray) {
    if (!tagsArray || !Array.isArray(tagsArray)) return '';
    return tagsArray.join(', ');
}

function showMessage(container, type, message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'}"></i>
        <span>${message}</span>
    `;
    
    // Remove existing messages
    const existingMessages = container.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());
    
    // Add new message
    container.insertBefore(messageDiv, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Form handlers
async function handleGenerateSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const title = formData.get('title');
    const notes = formData.get('notes');
    const tags = parseTags(formData.get('tags'));
    
    showLoading('Generating blog post with AI...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/blog/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title,
                notes,
                tags
            }),
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (data.success) {
            displayGenerateResult(data);
            showMessage(document.getElementById('generate'), 'success', 'Blog post generated successfully!');
        } else {
            showMessage(document.getElementById('generate'), 'error', `Generation failed: ${data.message}`);
        }
        
    } catch (error) {
        hideLoading();
        showMessage(document.getElementById('generate'), 'error', `Error: ${error.message}`);
    }
}

async function handlePublishSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const title = formData.get('title');
    const content = formData.get('content');
    const tags = parseTags(formData.get('tags'));
    const coverImageUrl = formData.get('cover_image_url') || null;
    
    showLoading('Publishing to Hashnode...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/blog/publish`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title,
                content,
                tags,
                cover_image_url: coverImageUrl
            }),
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (response.ok && data.success) {
            displayPublishResult(data);
            showMessage(document.getElementById('publish'), 'success', 'Blog post published successfully!');
            event.target.reset(); // Clear the form
        } else {
            const errorMessage = data.detail?.message || data.message || 'Publishing failed';
            showMessage(document.getElementById('publish'), 'error', errorMessage);
        }
        
    } catch (error) {
        hideLoading();
        showMessage(document.getElementById('publish'), 'error', `Error: ${error.message}`);
    }
}

async function handleComboSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const title = formData.get('title');
    const notes = formData.get('notes');
    const tags = parseTags(formData.get('tags'));
    
    showLoading('Generating and publishing blog post...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/blog/generate-and-publish`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title,
                notes,
                tags,
                publish_immediately: true
            }),
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (data.success) {
            displayComboResult(data);
            showMessage(document.getElementById('combo'), 'success', 'Blog post generated and published successfully!');
            event.target.reset(); // Clear the form
        } else {
            showMessage(document.getElementById('combo'), 'error', `Process failed: ${data.message}`);
        }
        
    } catch (error) {
        hideLoading();
        showMessage(document.getElementById('combo'), 'error', `Error: ${error.message}`);
    }
}

// Result display functions
function displayGenerateResult(data) {
    const resultCard = document.getElementById('generateResult');
    const preview = document.getElementById('generatePreview');
    
    const blogPost = data.blog_post;
    
    // Store the current blog post data for copying
    currentBlogPost = blogPost;
    
    preview.innerHTML = `
        <div class="blog-info">
            <h4>Blog Post Details</h4>
            <p><strong>Title:</strong> ${blogPost.title}</p>
            <p><strong>Tags:</strong> ${formatTags(blogPost.tags) || 'None'}</p>
            <p><strong>Generation Time:</strong> ${data.generation_time_seconds?.toFixed(2)}s</p>
            ${blogPost.summary ? `<p><strong>Summary:</strong> ${blogPost.summary}</p>` : ''}
        </div>
        <div class="content-preview">
            <h4>Content Preview</h4>
            <div class="blog-preview">${markdownToHtml(blogPost.content)}</div>
        </div>
        <div class="actions" style="margin-top: 20px;">
            <button class="btn btn-secondary" id="copyToPublishBtn">
                <i class="fas fa-copy"></i> Copy to Publish Form
            </button>
        </div>
    `;
    
    // Add event listener for the copy button
    const copyBtn = document.getElementById('copyToPublishBtn');
    copyBtn.addEventListener('click', () => {
        copyToPublishForm(currentBlogPost.title, currentBlogPost.content, formatTags(currentBlogPost.tags));
    });
    
    resultCard.style.display = 'block';
}

function displayPublishResult(data) {
    const resultCard = document.getElementById('publishResult');
    const preview = document.getElementById('publishPreview');
    
    preview.innerHTML = `
        <div class="message success">
            <i class="fas fa-check-circle"></i>
            <span>Successfully published to Hashnode!</span>
        </div>
        <div class="publish-details">
            <p><strong>Post ID:</strong> ${data.post_id}</p>
            <p><strong>Published URL:</strong> <a href="${data.post_url}" target="_blank" class="link">${data.post_url}</a></p>
            <div style="margin-top: 15px;">
                <a href="${data.post_url}" target="_blank" class="btn btn-secondary">
                    <i class="fas fa-external-link-alt"></i> View Published Post
                </a>
            </div>
        </div>
    `;
    
    resultCard.style.display = 'block';
}

function displayComboResult(data) {
    const resultCard = document.getElementById('comboResult');
    const preview = document.getElementById('comboPreview');
    
    const blogPost = data.blog_post;
    
    preview.innerHTML = `
        <div class="message success">
            <i class="fas fa-rocket"></i>
            <span>Blog post generated and published successfully!</span>
        </div>
        <div class="combo-details">
            <h4>Generated Content</h4>
            <p><strong>Title:</strong> ${blogPost.title}</p>
            <p><strong>Tags:</strong> ${formatTags(blogPost.tags) || 'None'}</p>
            <p><strong>Generation Time:</strong> ${data.generation_time_seconds?.toFixed(2)}s</p>
            
            ${data.hashnode_url ? `
                <h4 style="margin-top: 20px;">Publication Details</h4>
                <p><strong>Published URL:</strong> <a href="${data.hashnode_url}" target="_blank" class="link">${data.hashnode_url}</a></p>
                <div style="margin-top: 15px;">
                    <a href="${data.hashnode_url}" target="_blank" class="btn btn-accent">
                        <i class="fas fa-external-link-alt"></i> View Published Post
                    </a>
                </div>
            ` : `
                <div class="message error" style="margin-top: 20px;">
                    <i class="fas fa-exclamation-triangle"></i>
                    <span>Blog post was generated but publishing failed. Check the logs for details.</span>
                </div>
            `}
            
            <div class="content-preview" style="margin-top: 20px;">
                <h4>Content Preview</h4>
                <div class="blog-preview">${markdownToHtml(blogPost.content)}</div>
            </div>
        </div>
    `;
    
    resultCard.style.display = 'block';
}

// Utility function to copy generated content to publish form
function copyToPublishForm(title, content, tags) {
    try {
        // Switch to publish tab
        const publishTab = document.querySelector('[data-tab="publish"]');
        if (publishTab) {
            publishTab.click();
        }
        
        // Wait a moment for tab to switch, then fill the form
        setTimeout(() => {
            const titleField = document.getElementById('publishTitle');
            const contentField = document.getElementById('publishContent');
            const tagsField = document.getElementById('publishTags');
            
            if (titleField && contentField && tagsField) {
                titleField.value = title || '';
                contentField.value = content || '';
                tagsField.value = tags || '';
                
                // Show confirmation
                showMessage(document.getElementById('publish'), 'success', 'Content copied to publish form successfully!');
                
                // Scroll to the top of the publish form
                const publishCard = document.querySelector('#publish .card');
                if (publishCard) {
                    publishCard.scrollIntoView({ behavior: 'smooth' });
                }
            } else {
                throw new Error('Could not find publish form fields');
            }
        }, 100);
        
    } catch (error) {
        console.error('Error copying to publish form:', error);
        showMessage(document.getElementById('generate'), 'error', 'Failed to copy content. Please try again.');
    }
}

// Simple markdown to HTML converter (basic implementation)
function markdownToHtml(markdown) {
    let html = markdown;
    
    // Headers
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    
    // Bold
    html = html.replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>');
    
    // Italic
    html = html.replace(/\*(.*)\*/gim, '<em>$1</em>');
    
    // Code blocks
    html = html.replace(/```([a-z]*)\n([\s\S]*?)```/gim, '<pre><code>$2</code></pre>');
    
    // Inline code
    html = html.replace(/`([^`]*)`/gim, '<code>$1</code>');
    
    // Line breaks
    html = html.replace(/\n/gim, '<br>');
    
    return html;
} 
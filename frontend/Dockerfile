# Use Alpine Python
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache curl

# Copy frontend files
COPY . .

# Expose port
EXPOSE 3003

# Use the existing launch script
CMD ["python", "launch.py"] 
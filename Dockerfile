# Multi-stage build for Django + React
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend files
COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .

# Build frontend
RUN npm run build

# Python backend stage
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy frontend build from previous stage
COPY --from=frontend-builder /app/frontend/dist ./backend/dist

# Collect static files
WORKDIR /app/backend
RUN mkdir -p staticfiles && python manage.py collectstatic --noinput 2>/dev/null || true

# Copy frontend built files to static
RUN mkdir -p staticfiles/dist && cp -r dist/* staticfiles/dist/ 2>/dev/null || true

WORKDIR /app

# Create startup script
RUN echo '#!/bin/bash\nset -e\ncd /app/backend\npython manage.py migrate --noinput\nexec gunicorn playto_pay.wsgi --bind 0.0.0.0:8000 --log-file -\n' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Start server with migrations
CMD ["/app/start.sh"]


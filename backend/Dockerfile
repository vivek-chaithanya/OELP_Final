# ---- Stage 1: Build frontend ----
    FROM node:20 AS frontend-build

    WORKDIR /app/frontend
    
    # Copy frontend files
    COPY frontend/web/package*.json ./
    COPY frontend/web/ ./
    
    # Install dependencies and build
    RUN npm ci
    RUN npm run build
    
    # ---- Stage 2: Setup backend ----
    FROM python:3.13-slim
    
    # Set environment variables
    ENV PYTHONUNBUFFERED=1 \
        DJANGO_SETTINGS_MODULE=agriplatform.settings.prod \
        DATABASE_URL=postgres://postgres:postgres@db:5432/agriplatform \
        REDIS_URL=redis://redis:6379/1 \
        SECRET_KEY='replace-with-your-secret-key' \
        ALLOWED_HOSTS='*' \
        CORS_ALLOWED_ORIGINS='*'
    
    # Set working directory
    WORKDIR /app/backend
    
    # Copy backend files
    COPY backend/ .
    
    # Copy built frontend into Django static files
    COPY --from=frontend-build /app/frontend/dist/ agriplatform/static/
    
    # Install Python dependencies
    RUN pip install --upgrade pip
    RUN pip install -r requirements.txt
    
    # Expose port
    EXPOSE 8000
    
    # Run migrations and start server
    CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn agriplatform.wsgi:application --bind 0.0.0.0:8000"]
    
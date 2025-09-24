# Stage 1: Build frontend
FROM node:20 AS frontend-build

WORKDIR /app/frontend

# Copy frontend package files and install dependencies
COPY frontend/web/package*.json ./
RUN npm ci

# Copy frontend source and build
COPY frontend/web/ ./
RUN npm run build

# Stage 2: Backend
FROM python:3.13-slim

WORKDIR /app

# System dependencies (optional, for psycopg2)
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy frontend build into Django static folder
COPY --from=frontend-build /app/frontend/dist ./static

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn agriplatform.wsgi:application --bind 0.0.0.0:8000"]

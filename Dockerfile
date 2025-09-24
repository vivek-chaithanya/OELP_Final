# syntax=docker/dockerfile:1

# Stage 1: Build frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/web/package*.json ./
RUN npm ci
COPY frontend/web/ ./
ARG VITE_API_BASE
ENV VITE_API_BASE=${VITE_API_BASE}
RUN npm run build

# Stage 2: Backend runtime
FROM python:3.13-slim AS backend
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev nginx supervisor \
    && rm -rf /var/lib/apt/lists/*

# Backend deps
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/backend/requirements.txt

# Copy backend code
COPY backend/ /app/backend/

# Copy built frontend to nginx root
COPY --from=frontend-builder /app/frontend/dist/ /var/www/html/

# Nginx config
RUN rm -f /etc/nginx/sites-enabled/default
COPY infra/nginx.conf /etc/nginx/conf.d/default.conf

# Supervisor config
COPY infra/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV DJANGO_SETTINGS_MODULE=agriplatform.settings.prod \
    PORT=8000

EXPOSE 8000 80

WORKDIR /app/backend

CMD ["/usr/bin/supervisord", "-n"]


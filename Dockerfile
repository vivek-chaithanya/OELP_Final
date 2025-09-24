# Stage 2: Backend
FROM python:3.13-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy frontend build into Django static folder
COPY --from=frontend-build /app/frontend/dist ./static

# Set environment variable
ENV DJANGO_SETTINGS_MODULE=agriplatform.settings.prod

# Expose port
EXPOSE 8000

# Run migrations and start Gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn agriplatform.wsgi:application --bind 0.0.0.0:8000"]

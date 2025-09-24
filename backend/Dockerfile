# syntax=docker/dockerfile:1
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app
ENV DJANGO_SETTINGS_MODULE=agriplatform.settings.prod
CMD ["bash", "-lc", "python manage.py migrate && gunicorn agriplatform.wsgi:application --bind 0.0.0.0:8000"]

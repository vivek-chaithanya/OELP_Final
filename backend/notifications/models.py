from django.db import models
from django.conf import settings


class NotificationTemplate(models.Model):
    name = models.CharField(max_length=120, unique=True)
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    channels = models.JSONField(default=list)  # ["push","email","sms"]


class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sent_notifications')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    template = models.ForeignKey(NotificationTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    channels = models.JSONField(default=list)
    scheduled_at = models.DateTimeField(blank=True, null=True)
    recurring_cron = models.CharField(max_length=100, blank=True)  # optional cron expr
    window_start = models.DateTimeField(blank=True, null=True)
    window_end = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

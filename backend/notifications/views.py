import os
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client as TwilioClient
from fcm_django.models import FCMDevice
from .models import NotificationTemplate, Notification
from .serializers import NotificationTemplateSerializer, NotificationSerializer
from accounts.permissions import IsAdminOrSuperAdmin


def send_email(to_email: str, subject: str, body: str):
    api_key = os.getenv('SENDGRID_API_KEY', '')
    if not api_key:
        return
    message = Mail(from_email='no-reply@agriplatform.com', to_emails=to_email, subject=subject, html_content=body)
    sg = SendGridAPIClient(api_key)
    sg.send(message)


def send_sms(to_phone: str, body: str):
    sid = os.getenv('TWILIO_SID', '')
    token = os.getenv('TWILIO_TOKEN', '')
    from_phone = os.getenv('TWILIO_FROM', '')
    if not sid or not token or not from_phone:
        return
    client = TwilioClient(sid, token)
    client.messages.create(to=to_phone, from_=from_phone, body=body)


def send_push(user, title: str, body: str):
    devices = FCMDevice.objects.filter(user=user)
    for d in devices:
        d.send_message(title=title, body=body)


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperAdmin]


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role and user.role.name in ("SuperAdmin", "Admin"):
            return Notification.objects.all()
        return Notification.objects.filter(receiver=user)

    def perform_create(self, serializer):
        notif = serializer.save(sender=self.request.user)
        if not notif.scheduled_at:
            self._send_now(notif)

    @action(detail=True, methods=['post'])
    def send_now(self, request, pk=None):
        notif = self.get_object()
        self._send_now(notif)
        return Response({"status": "sent"})

    def _send_now(self, notif: Notification):
        channels = notif.channels or []
        subject = notif.subject or (notif.template.subject if notif.template else "")
        body = notif.body or (notif.template.body if notif.template else "")
        if "email" in channels and notif.receiver.email:
            send_email(notif.receiver.email, subject, body)
        if "sms" in channels and notif.receiver.phone:
            send_sms(notif.receiver.phone, body)
        if "push" in channels:
            send_push(notif.receiver, subject or "Notification", body)
        notif.sent_at = timezone.now()
        notif.save()
from django.shortcuts import render

# Create your views here.

import os
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from twilio.rest import Client as TwilioClient
from .serializers import RegisterSerializer, UserSerializer, GoogleAuthSerializer, PhoneStartSerializer, PhoneVerifySerializer, AssignRoleSerializer
from .models import Role, Region
from .permissions import IsAdminOrSuperAdmin


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user


class GoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["id_token"]
        client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        try:
            idinfo = google_id_token.verify_oauth2_token(token, google_requests.Request(), client_id)
            sub = idinfo["sub"]
            email = idinfo.get("email")
            name = idinfo.get("name", "")
            username = f"google_{sub}"
            user, _ = User.objects.get_or_create(google_sub=sub, defaults={
                "username": username,
                "email": email or f"{username}@agriplatform.com",
                "first_name": name.split(" ")[0] if name else "",
                "last_name": " ".join(name.split(" ")[1:]) if name and len(name.split(" ")) > 1 else "",
                "alias_email": f"{username}@agriplatform.com",
            })
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class PhoneStartView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PhoneStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        client = TwilioClient(os.getenv("TWILIO_SID", ""), os.getenv("TWILIO_TOKEN", ""))
        service_sid = os.getenv("TWILIO_VERIFY_SID", "")
        verification = client.verify.v2.services(service_sid).verifications.create(to=phone, channel="sms")
        return Response({"status": verification.status})


class PhoneVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PhoneVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        code = serializer.validated_data["code"]
        client = TwilioClient(os.getenv("TWILIO_SID", ""), os.getenv("TWILIO_TOKEN", ""))
        service_sid = os.getenv("TWILIO_VERIFY_SID", "")
        verification_check = client.verify.v2.services(service_sid).verification_checks.create(to=phone, code=code)
        if verification_check.status == "approved":
            user, _ = User.objects.get_or_create(username=f"phone_{phone}", defaults={
                "email": f"{phone}@agriplatform.com",
                "phone": phone,
                "alias_email": f"phone_{phone}@agriplatform.com",
            })
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"detail": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)


class AssignRoleView(APIView):
    permission_classes = [IsAdminOrSuperAdmin]

    def post(self, request):
        serializer = AssignRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(id=serializer.validated_data['user_id'])
        role = Role.objects.get(id=serializer.validated_data['role_id'])
        region = None
        if serializer.validated_data.get('region_id'):
            region = Region.objects.get(id=serializer.validated_data['region_id'])
        user.role = role
        user.region = region
        user.save()
        return Response(UserSerializer(user).data)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperAdmin]
    serializer_class = GoogleAuthSerializer  # placeholder to satisfy DRF typing

    def get_serializer_class(self):
        from .serializers import RoleSerializer
        return RoleSerializer


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperAdmin]
    serializer_class = GoogleAuthSerializer

    def get_serializer_class(self):
        from .serializers import RegionSerializer
        return RegionSerializer
from django.shortcuts import render

# Create your views here.

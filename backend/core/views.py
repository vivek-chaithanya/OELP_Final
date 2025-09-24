from rest_framework import viewsets, permissions
from accounts.permissions import RegionScopedPermission, IsAdminOrSuperAdmin
from .models import Farm, Field, Crop, CropVariety, IrrigationMethod, Asset, CropLifecycleDates, SoilReport
from .serializers import (
    FarmSerializer,
    FieldSerializer,
    CropSerializer,
    CropVarietySerializer,
    IrrigationMethodSerializer,
    AssetSerializer,
    CropLifecycleDatesSerializer,
    SoilReportSerializer,
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        return True


class FarmViewSet(viewsets.ModelViewSet):
    serializer_class = FarmSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Farm.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FieldViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) and user.role:
            if user.role.name == 'SuperAdmin':
                return Field.objects.all()
            if user.role.name == 'Admin' and user.region_id:
                return Field.objects.filter(farm__region_id=user.region_id)
        return Field.objects.filter(farm__owner=user)


class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperAdmin]


class CropVarietyViewSet(viewsets.ModelViewSet):
    queryset = CropVariety.objects.all()
    serializer_class = CropVarietySerializer
    permission_classes = [permissions.IsAuthenticated]


class IrrigationMethodViewSet(viewsets.ModelViewSet):
    queryset = IrrigationMethod.objects.all()
    serializer_class = IrrigationMethodSerializer
    permission_classes = [permissions.IsAuthenticated]


class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) and user.role:
            if user.role.name == 'SuperAdmin':
                return Asset.objects.all()
            if user.role.name == 'Admin' and user.region_id:
                return Asset.objects.filter(farm__region_id=user.region_id)
        return Asset.objects.filter(farm__owner=user)


class CropLifecycleDatesViewSet(viewsets.ModelViewSet):
    serializer_class = CropLifecycleDatesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) and user.role:
            if user.role.name == 'SuperAdmin':
                return CropLifecycleDates.objects.all()
            if user.role.name == 'Admin' and user.region_id:
                return CropLifecycleDates.objects.filter(field__farm__region_id=user.region_id)
        return CropLifecycleDates.objects.filter(field__farm__owner=user)


class SoilReportViewSet(viewsets.ModelViewSet):
    serializer_class = SoilReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        field_id = self.request.query_params.get('fieldId')
        if getattr(user, 'role', None) and user.role:
            if user.role.name == 'SuperAdmin':
                qs = SoilReport.objects.all()
                return qs.filter(field_id=field_id) if field_id else qs
            if user.role.name == 'Admin' and user.region_id:
                qs = SoilReport.objects.filter(field__farm__region_id=user.region_id)
                return qs.filter(field_id=field_id) if field_id else qs
        qs = SoilReport.objects.filter(field__farm__owner=user)
        return qs.filter(field_id=field_id) if field_id else qs
from django.shortcuts import render

# Create your views here.

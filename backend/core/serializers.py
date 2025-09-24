from rest_framework import serializers
from .models import Farm, Field, Crop, CropVariety, IrrigationMethod, Asset, CropLifecycleDates, SoilReport


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = "__all__"


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = "__all__"


class CropVarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = CropVariety
        fields = "__all__"


class IrrigationMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrrigationMethod
        fields = "__all__"


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"


class CropLifecycleDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropLifecycleDates
        fields = "__all__"


class SoilReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilReport
        fields = "__all__"


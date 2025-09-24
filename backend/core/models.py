from django.db import models
from django.conf import settings
from accounts.models import Region


class Farm(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="farms")
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Field(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="fields")
    name = models.CharField(max_length=200)
    area_hectares = models.DecimalField(max_digits=10, decimal_places=2)
    geojson = models.JSONField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.farm.name} - {self.name}"


class Crop(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class CropVariety(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="varieties")
    name = models.CharField(max_length=120)
    maturity_days = models.IntegerField(default=0)

    class Meta:
        unique_together = ("crop", "name")

    def __str__(self) -> str:
        return f"{self.crop.name} - {self.name}"


class IrrigationMethod(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.name


class Asset(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="assets")
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=120)
    purchase_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class CropLifecycleDates(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="lifecycles")
    crop_variety = models.ForeignKey(CropVariety, on_delete=models.SET_NULL, null=True, blank=True)
    sowing_date = models.DateField()
    expected_harvest_date = models.DateField(blank=True, null=True)
    irrigation_method = models.ForeignKey(IrrigationMethod, on_delete=models.SET_NULL, null=True, blank=True)


class SoilReport(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="soil_reports")
    report_date = models.DateField()
    ph = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    nitrogen = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    phosphorus = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    potassium = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    organic_matter = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True)
from django.db import models

# Create your models here.

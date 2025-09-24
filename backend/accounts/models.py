from django.contrib.auth.models import AbstractUser
from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    alias_email = models.EmailField(blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    google_sub = models.CharField(max_length=255, blank=True, null=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self) -> str:
        return self.username
from django.db import models

# Create your models here.

from django.contrib import admin
from .models import CustomUser, Role, Region


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "region")
    search_fields = ("username", "email")


admin.site.register(Role)
admin.site.register(Region)
from django.contrib import admin

# Register your models here.

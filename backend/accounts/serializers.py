from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Role, Region


User = get_user_model()


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name"]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "description"]


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "alias_email",
            "first_name",
            "last_name",
            "role",
            "region",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "phone", "first_name", "last_name"]

    def validate_password(self, value: str) -> str:
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        # Issue alias email
        user.alias_email = f"{user.username}@agriplatform.com"
        user.save()
        return user


class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role_id = serializers.IntegerField()
    region_id = serializers.IntegerField(required=False, allow_null=True)


class GoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField()


class PhoneStartSerializer(serializers.Serializer):
    phone = serializers.CharField()


class PhoneVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()


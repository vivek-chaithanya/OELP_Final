from rest_framework import serializers
from .models import MainPlan, TopUpPlan, EnterprisePlan, UserPlan, FeatureUsage, Payment


class MainPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPlan
        fields = '__all__'


class TopUpPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopUpPlan
        fields = '__all__'


class EnterprisePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnterprisePlan
        fields = '__all__'


class UserPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlan
        fields = '__all__'
        read_only_fields = ('user', 'status', 'start_date')


from django.db import models
from django.conf import settings


class MainPlan(models.Model):
	name = models.CharField(max_length=100, unique=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	features = models.JSONField(default=dict)
	active = models.BooleanField(default=True)


class TopUpPlan(models.Model):
	name = models.CharField(max_length=100, unique=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quota = models.IntegerField(default=0)
	active = models.BooleanField(default=True)


class EnterprisePlan(models.Model):
	name = models.CharField(max_length=100, unique=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	terms = models.TextField(blank=True)
	active = models.BooleanField(default=True)


class UserPlan(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	plan_type = models.CharField(max_length=20, choices=[("main","main"),("topup","topup"),("enterprise","enterprise")])
	plan_id = models.IntegerField()
	start_date = models.DateField(auto_now_add=True)
	end_date = models.DateField(blank=True, null=True)
	status = models.CharField(max_length=20, default="active")
	metadata = models.JSONField(default=dict, blank=True)


class FeatureUsage(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	feature = models.CharField(max_length=100)
	count = models.IntegerField(default=0)
	period = models.DateField()


class Payment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	currency = models.CharField(max_length=10, default="INR")
	gateway = models.CharField(max_length=50, default="razorpay")
	order_id = models.CharField(max_length=100, blank=True, null=True)
	payment_id = models.CharField(max_length=100, blank=True, null=True)
	receipt = models.CharField(max_length=100, blank=True, null=True)
	status = models.CharField(max_length=20, default="created")
	created_at = models.DateTimeField(auto_now_add=True)
	refunded = models.BooleanField(default=False)
	refund_id = models.CharField(max_length=100, blank=True, null=True)
	meta = models.JSONField(default=dict, blank=True)

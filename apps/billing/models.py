
    # Used for subscription
from django.db import models
from django.utils import timezone

class Subscription(models.Model):
    tenant=models.OneToOneField("tenants.Tenant",on_delete=models.CASCADE)
    plan=models.ForeignKey("subscriptions.Plan",on_delete=models.SET_NULL,null=True,blank=True)

    start_date=models.DateTimeField(default=timezone.now)
    end_date=models.DateTimeField(null=True,blank=True)

    is_active=models.BooleanField(default=True)
    is_trial=models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subscription for {self.tenant.name}"
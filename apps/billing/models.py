
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
    
class Invoice(models.Model):
    STATUS_PENDING="pending"
    STATUS_PAID="paid"
    STATUS_FAILED="failed"

    STATUS_CHOICES= [
        (STATUS_PENDING,"pending"),
        (STATUS_PAID,"paid"),
        (STATUS_FAILED,"Failed"),
    ]

    tenant = models.ForeignKey("tenants.Tenant",on_delete=models.CASCADE, related_name="invoices")
    plan=models.ForeignKey("subscriptions.Plan",on_delete=models.SET_NULL,null=True,blank=True)
    subscription=models.ForeignKey("billing.Subscription",on_delete=models.SET_NULL,null=True,blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES,default=STATUS_PENDING)

    created_at=models.DateTimeField(auto_now_add=True)
    due_date= models.DateTimeField(default=timezone.now)
    paid_at=models.DateTimeField(null=True,blank=True)

    class Meta:
        ordering =("-created_at",)

    def mark_paid(self):
        self.status=self.STATUS_PAID
        self.paid_at=timezone.now()
        self.save()

    def mark_failed(self):
        self.status=self.STATUS_FAILED
        self.save()

    def __str__(self):
        return f"Invoice #{self.id} - {self.tenant} - {self.status}"
    
class InvoiceService:
    @staticmethod
    def generate_invoice(subscription):
        return Invoice.objects.create(
            tenant=subscription.tenant,
            plan=subscription.plan,
            subscription=subscription,
            amount=subscription.plan.price,
            due_date=timezone.now(),
            status=Invoice.STATUS_PENDING
        )
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Tenant(models.Model):
    name=models.CharField(max_length=255,unique=True)
    slug=models.SlugField(max_length=160,unique=True,blank=True)
    owner=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True,related_name='owned_tenants')
    domain=models.CharField(max_length=255,blank=True,null=True,help_text='optional custom domain for this tenant')
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering =('-created_at',)

    def save(self,*args, **kwargs):
        if not self.slug:
            base=slugify(self.name)[:140]
            slug=base
            counter=1
            while Tenant.objects.filter(slug=slug).exists():
                slug=f"{base}-{counter}"
                counter+=1
            self.slug = slug
        super().save(*args,**kwargs)

class Membership(models.Model):
    ROLE_OWNER="owner"
    ROLE_ADMIN="admin"
    ROLE_USER="user"

    ROLE_CHOICES=[
        (ROLE_OWNER,"Owner"),
        (ROLE_ADMIN,"Admin"),
        (ROLE_USER,"User"),

    ]

    tenant=models.ForeignKey("tenants.Tenant",on_delete=models.CASCADE,related_name="memberships")
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="memberships")
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default=ROLE_USER)

    class Meta:
        unique_together = ("tenant","user")

    def __str__(self):
        return f"{self.user.email} -> {self.tenant.name} ({self.role})"

@receiver(post_save,sender=Tenant)
def create_owner_membership(sender, instance,created,**kwargs):
    if created and instance.owner:
        from tenants.models import Membership
        Membership.objects.get_or_create(
            tenant=instance,
            user=instance.owner,
            defaults={"role":Membership.ROLE_OWNER}
        )
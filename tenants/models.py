from django.db import models
from django.conf import settings
from django.utils.text import slugify
# Create your models here.

class Tenant(models.Model):
    name=models.CharField(max_length=150)
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

    def __str__(self):
        return f"{self.name} ({self.slug})"

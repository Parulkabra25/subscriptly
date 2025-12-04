from django.db import models

# Create your models here.
class Plan(models.Model):
    name=models.CharField(max_length=100,unique=True)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    duration_days=models.PositiveIntegerField()
    quota=models.PositiveIntegerField(help_text="Allowed resources")
    description = models.TextField(blank=True)
    is_active=models.BooleanField(default=True)


    def __str__(self):
        return self.name
    




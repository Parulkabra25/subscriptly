from rest_framework import serializers
from .models import Tenant
from django.contrib.auth import get_user_model

User=get_user_model()

class TenantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tenant
        fields=('id','name','slug','domain')
        read_only_fields=('id','slug')

    def validate_name(self,value):
        if len(value) <3:
            raise serializers.ValidationError('Tenant name too short')
        return value
    
class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tenant
        fields=('id','name','slug','domain','owner','is_active','created_at')
        read_only_fields =('id', 'slug', 'owner','is_active','created_at')

        
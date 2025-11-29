from django.contrib import admin
from .models import Tenant

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display=('id','name','slug','owner','is_active','created_at')
    search_fields=('name','slug','owner__email')
    list_filter=('is_active','created_at')
    list_display_links=('name',)

    
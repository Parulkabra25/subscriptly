from django.contrib import admin
from apps.subscriptions.models import Plan
from .models import Subscription
# Register your models here.

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display=("name","price","duration_days","quota","is_active")
    list_filter=("is_active",)
    search_fields=("name",)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display=("tenant","plan","start_date","end_date","is_active","is_trial")
    list_filter=("is_active","is_trial")
    search_fields=("tenant_name","plan_name")
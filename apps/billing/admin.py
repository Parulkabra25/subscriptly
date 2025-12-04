from django.contrib import admin
from .models import Plan
# Register your models here.

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display=("name","price","duration_days","quota","is_active")
    list_filter=("is_active",)
    search_fields=("name",)
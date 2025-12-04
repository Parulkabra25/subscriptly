from django.urls import path
from .views import TenantMeView,TenantCreateView

urlpatterns=[
    path("me/",TenantMeView.as_view(),name="tenant-me"),
    path("create/",TenantCreateView.as_view(),name="tenant-create"),    
]


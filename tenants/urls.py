from django.urls import path
from .views import TenantMeView,TenantCreateView
from .views import TenantAdminExampleView

urlpatterns=[
    path("me/",TenantMeView.as_view(),name="tenant-me"),
    path("create/",TenantCreateView.as_view(),name="tenant-create"),   
    path("admin/check/",TenantAdminExampleView.as_view(),name="tenant-admin-check"), 
]


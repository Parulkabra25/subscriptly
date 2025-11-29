"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
# from drf_spectacular.openapi import AutoSchema
# from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from rest_framework.documentation import include_docs_urls
# from django.views.generic import TemplateView
# from drf_spectacular.utils import extend_schema

# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularSwaggerView,
#     SpectacularRedocView,
# )

# TokenObtainPairView.schema = AutoSchema()
# TokenRefreshView.schema = AutoSchema()
# TokenVerifyView.schema = AutoSchema()

urlpatterns = [
    path('admin/', admin.site.urls),

      
    # JWT Auth endpoints
    path('api/auth/login/',TokenObtainPairView.as_view(),name='login'),
    path('api/auth/refresh/',TokenRefreshView.as_view(),name='refresh'),
    path('api/auth/verify/',TokenVerifyView.as_view(),name='verify'),
    
    # Include app URLS
    path('api/users/', include('apps.users.urls')),

     # Built-in DRF docs
    path('api/docs/', include_docs_urls(title="Subscriptly API")),

    # # OpenAPI Schema
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # # API Docs (ReDoc)
    # path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),   

    #  # Swagger UI (CDN version - ALWAYS WORKS)
    # path(
    #     'api/docs/',
    #     TemplateView.as_view(
    #         template_name='swagger.html',
    #         extra_context={'schema_url': 'schema'},
    #     ),
    #     name='swagger-ui'
    # ), 

    path('api/tenants/', include('tenants.urls')),
    
]
    

from django.urls import path
from .views import create_order_api

urlpatterns= [
    path('create-order/',create_order_api,name='create-order'),
]

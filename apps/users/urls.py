from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,ProfileView


router=DefaultRouter()
router.register(r'users',UserViewSet)

urlpatterns=[
    path('profile/',ProfileView.as_view(),name='profile'),
]

urlpatterns += router.urls
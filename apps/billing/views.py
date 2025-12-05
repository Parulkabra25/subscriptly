from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny,IsAdminUser
from apps.subscriptions.models import Plan
from .serializers import PlanSerializer

# Create your views here.
class PlanViewSet(viewsets.ModelViewSet):
    queryset=Plan.objects.all()
    serializer_class=PlanSerializer

    def get_permissions(self):
        if self.request.method in ('GET','HEAD','OPTIONS'):
            return [AllowAny()]
        return [IsAdminUser()]
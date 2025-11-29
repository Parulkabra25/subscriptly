from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction

from .serializers import TenantCreateSerializer,TenantSerializer
# Create your views here.

class TenantCreateView(APIView):
    permission_classes=(IsAuthenticated,)

    def post(self,request):
        serializer=TenantCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            tenant=serializer.save(owner=request.user)

            try:
                user=request.user
                if hasattr(user,'tenant'):
                    user.tenant=tenant
                    user.save(update_fields=['tenant'])
            except Exception:
                pass

        out=TenantSerializer(tenant,context={'request':request}).data
        return Response(out, status=status.HTTP_201_CREATED)
    

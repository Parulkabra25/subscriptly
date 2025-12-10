from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import TenantCreateSerializer, TenantSerializer
from .permissions import IsTenantAdmin

from apps.billing.models import Subscription
from django.utils import timezone
from datetime import timedelta

class TenantMeView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        tenant=getattr(request,"tenant",None)
        if tenant is None:
            return Response({"detail":"Tenant not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(TenantSerializer(tenant).data)
    

TRIAL_DAYS=7

def assign_trial_subscription(tenant):
    Subscription.objects.create(
        tenant=tenant,
        plan=None,
        is_trial=True,
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=TRIAL_DAYS),
        is_active=True

    )

class TenantCreateView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request):
        serializer=TenantCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tenant=serializer.save(owner=request.user)
        

        # Assign free trial
        assign_trial_subscription(tenant)
        return Response(TenantSerializer(tenant).data,status=status.HTTP_201_CREATED)
    
class TenantAdminExampleView(APIView):
    permission_classes=[IsAuthenticated,IsTenantAdmin]

    def get(self,request):
        return Response({
            "message":"You are an admin or owner",
            "tenant":request.tenant.slug
        })

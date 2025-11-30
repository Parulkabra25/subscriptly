from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import TenantSerializer

class TenantMeView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        tenant=getattr(request,"tenant",None)
        if tenant is None:
            return Response({"detail":"Tenant not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(TenantSerializer(tenant).data)
    
    
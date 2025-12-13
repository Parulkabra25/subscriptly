from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import create_order
# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_api(request):
    amount=request.data.get("amount",0)

    if not amount:
        return Response({"error:" "Amount is required"}, status=400)
    
    order=create_order(amount)
    return Response(order)



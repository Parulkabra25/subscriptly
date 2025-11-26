from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset= User.objects.all()
    serializer_class=UserSerializer

# Add this for /profile/endpoint
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProfileView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        serializer=UserSerializer(request.user)
        return Response(serializer.data)
    
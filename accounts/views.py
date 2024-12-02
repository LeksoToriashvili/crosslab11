from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserRegisterSerializer, CustomUserUpdateSerializer
from rest_framework import status


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow anyone to register
    http_method_names = ['post', 'put', 'patch']  # Only allow these methods

    # Registration action
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = CustomUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'detail': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update action
    @action(detail=True, methods=['put', 'patch'])
    def update_profile(self, request, pk=None):
        user = self.get_object()  # Get the user instance by primary key
        serializer = CustomUserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'User profile updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

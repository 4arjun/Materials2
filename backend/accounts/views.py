from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def changeUsername(request):
    try:
        new_username = request.data.get('username')
        
        if not new_username:
            return Response(
                {"error": "Username is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not new_username.strip():
            return Response(
                {"error": "Username cannot be empty"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
            return Response(
                {"error": "Username already exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(new_username) < 3:
            return Response(
                {"error": "Username must be at least 3 characters long"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user
        user.username = new_username
        user.save()
        
        return Response(
            {"message": "Username changed successfully", "new_username": new_username}, 
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {"error": "An error occurred while changing username"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
 


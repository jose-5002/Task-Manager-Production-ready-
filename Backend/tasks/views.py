from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.authtoken.models import Token

from .models import Task, Tag
from rest_framework import serializers
from .serializers import TaskSerializer, TagSerializer, CustomUserSerializer, RegisterUserSerializer, ProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
def register_user(request):
    serializer = RegisterUserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        token,_ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key,'user' : CustomUserSerializer(user).data}, status=201)
    
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()
    if user and user.check_password(password):
        token,_ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'user' : CustomUserSerializer(user).data}, status=200)
    
    return Response({'error': 'Invalid Credentials'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    profile_data = request.data

    serializer = ProfileSerializer(user, data=profile_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    
    return Response(serializer.errors, status=400)
    
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from .permission import IsOwner
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet 
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Task, Tag, Profile
from rest_framework import serializers
from .serializers import TaskSerializer, TagSerializer, CustomTokenPairSerializer, RegisterUserSerializer, ProfileSerializer, AssignTaskSerializer
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

User = get_user_model()

#LOGIN
class login_view(TokenObtainPairView):
    serializer_class = CustomTokenPairSerializer

#TASK
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'priority']
    ordering_fields = [ 'due_on', 'priority', 'created_on']

    def get_queryset(self): # What data does he have access?
        return Task.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):  # Who owns the data
        serializer.save(owner = self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.completed = "done"
        task.save()
        return Response({"message": "Task marked as completed"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        task = self.get_object()
        if request.user.status != 'active':
            return Response({"error": "Only active users can assign tasks."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AssignTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(id=serializer.validated_data['user_id'])
        task.assigned_to = user
        task.save()
        return Response({"message": f"Task assigned to {user.username}"}, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['post'])
    def unassign(self, request, pk=None):
        task = self.get_object()
        task.assigned_to = None
        task.save()
        return Response({"message": "Task unassigned"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def add_tag(self, request, pk=None):
        task = self.get_object()
        task_name = request.data.get('name')

        tag,_ = Tag.objects.get_or_create(name=task_name)
        task.tags.add(tag)
        return Response({"message": "Tag added to task"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def remove_tag(self, request, pk=None):
        task = self.get_object()
        tag_name = request.data.get('name')

        tag = Tag.objects.filter(name=tag_name).first()
        task.tags.remove(tag)
        return Response({"message": "Tag removed from task"}, status=status.HTTP_200_OK)

#Sign up/ Register
@api_view(['POST'])
def register_user(request):
    serializer = RegisterUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "User registered successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
#Tag
class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

#Profile
class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = IsAuthenticated

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)
    
    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


# @api_view(['POST'])
# def login_user(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     user = User.objects.filter(email=email).first()
#     if user and user.check_password(password):
#         token,_ = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key,'user' : CustomUserSerializer(user).data}, status=200)
    
#     return Response({'error': 'Invalid Credentials'}, status=400)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def update_profile(request):
#     user = request.user
#     profile_data = request.data

#     serializer = ProfileSerializer(user, data=profile_data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=200)
    
#     return Response(serializer.errors, status=400)
    
from .models import Task, Tag, Profile
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
User = get_user_model()
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#LOGIN
class CustomTokenPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email = email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        
        data = super().validate(attrs)
        data['user_id'] = user.id
        data['email'] = user.email

        return data

#TASK SERIALIZER
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner','created_on', 'updated_on' ]

    def validate_due_on(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
    
    def validate_priority(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Priority must be between 1 and 5.")
        return value

class AssignTaskSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")
        return value
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


#Sign up/ Register
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # user = User.objects.create_user(**validated_data)
        return user
    
#Profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['work_status', 'profile_picture', 'phone_number']
    

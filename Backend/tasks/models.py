from django.db import models
from django.contrib.auth.models import AbstractUser 

import datetime

Priority_Choices=[
    ('H', 'High'),
    ('M', 'Medium'),
    ('L', 'Low')
]

user_status_choices = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('banned', 'Banned'),
]

work_status_choices = [
    ('manager', 'Manager'),
    ('employee', 'Employee'),
    ('intern', 'Intern'),
    ('student', 'Student'),
    ('freelancer', 'Freelancer'),
    ('unemployed', 'Unemployed'),
]

# models.Choices('High', 'Low', 'Medium')
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=10)
    Tasks = models.ManyToManyField('Task', related_name='tags', blank=True)

class Task(models.Model):
    Title = models.CharField(max_length=30)
    Description = models.TextField(max_length=300)
    Due_Date = models.DateField()
    Created_Date = models.DateTimeField(auto_now_add=True)
    Completed = models.BooleanField(default=False)
    Priority = models.CharField(max_length=1, choices=Priority_Choices, default='M')
    Tags = models.ManyToManyField(Tag, related_name='tasks')

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=10, choices=user_status_choices, default='active', editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    work_status = models.CharField(max_length=10, choices=work_status_choices, default='employee')
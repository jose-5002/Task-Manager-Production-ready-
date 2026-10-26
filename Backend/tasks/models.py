from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser 

import datetime
User = settings.AUTH_USER_MODEL

user_status_choices = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('banned', 'Banned'),
]
# models.Choices('High', 'Low', 'Medium')
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    
    priority_choices=[ (1, 'Low'),  (2, 'Medium'), (3, 'High'), (4, 'Urgent'), (5, 'Critical') ] 

    task_status=[
        ('to_do', 'To do'),
        ('in_progress', 'In progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=30)
    description = models.TextField(max_length=300, default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks")
    due_on = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    completed = models.CharField(max_length=15, choices=task_status, default='to_do')
    priority = models.PositiveSmallIntegerField(choices=priority_choices, default=3)
    tags = models.ManyToManyField(Tag, null=True, blank=True, related_name='tasks')
    reminder_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['due_on', 'priority']
    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=10, choices=user_status_choices, default='active', editable=False)
    # AbstractUser` gives you `password`, `is_staff`, `is_active`, `is_superuser`, `date_joined`, `last_login` for free
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Profile(models.Model):

    work_status_choices = [
    ('manager', 'Manager'),
    ('employee', 'Employee'),
    ('intern', 'Intern'),
    ('student', 'Student'),
    ('freelancer', 'Freelancer'),
    ('unemployed', 'Unemployed'),
]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    work_status = models.CharField(max_length=10, choices=work_status_choices, default='employee')

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6)
    issued_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self): 
#         Implements a business rule directly on the model — a clean pattern called a model
# method. The logic lives close to the data it describes
        expiration_time = self.issued_at + datetime.timedelta(minutes=2)
        return datetime.datetime.now(datetime.timezone.utc) < expiration_time and not self.is_used
    
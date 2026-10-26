from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser, Task
from django.utils import timezone
from datetime import timedelta


# Create your tests here.
class Testcheck(TestCase):
    def test_sanity(self):
        self.assertTrue(True)
    
class TaskAPITestCase(TestCase):
    def setUp(self):  #Create resources to be used in the tests
        self.user = CustomUser.objects.create_user(username='testuser', email='user@test.com', password='pass1234')
        self.task = Task.objects.create(title='Test Task', description='Test Description', owner=self.user, due_on=timezone.now().date() + timedelta(days=1))
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_inactive_user_cannot_assign_task(self):
        # Set user status to inactive
        self.user.status = 'inactive'
        self.user.save()

        # Attempt to assign a task
        response = self.client.post(f'/tasks/{self.task.id}/assign/', {'user_id': self.user.id})

        # Check that the response indicates the user is inactive
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('Only active users can assign tasks', response.data['detail'])

    def test_active_user_can_assign_task(self):
        self.user.status = 'active'
        self.user.save()

        # Attempt to assign a task
        response = self.client.post(f'/tasks/{self.task.id}/assign/', {'user_id': self.user.id})

        # Check that the response indicates the user is inactive
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owners_only_access_task(self):
        user2 = CustomUser.objects.create_user(username='testuser2', email='user2@test.com', password='pass1234')
        self.client.force_authenticate(user=user2)
        response = self.client.get(f'/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        


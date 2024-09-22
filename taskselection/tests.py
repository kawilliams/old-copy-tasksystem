# from django.test import TestCase
# from rest_framework import status
# from rest_framework.test import APITestCase

# # class LoginTestCase(TestCase):
#   # def test_login_success(self):
#     # pass
#   # def test_login_failure(self):
#     # pass
#   # def test_logout(self):
#     # pass

# class TaskSelectionTestCase(APITestCase):
#   def test_list_available_tasks(self):
#     res = self.client.get('/available_tasks')
#     self.assertEqual(res.status_code, status.HTTP_200_OK)
#     self.assertEqual(len(res.data), 4)

#   def test_list_user_tasks(self):
#     res = self.client.get('/selected_tasks')
#     self.assertEqual(res.status_code, status.HTTP_200_OK)
#     self.assertEqual(len(res.data), 2)

#   def test_accept_task_available(self):
#     res = self.client.get('/selected_task/3')
#     self.assertEqual(res.status_code, status.HTTP_200_OK)
#     self.assertEqual(len(res.data), 2)

#   def test_accept_task_unavailable(self):
#     res = self.client.get('/selected_task/12')
#     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

#   def test_remove_task_success(self):
#     res = self.client.get('/selected_task/9')
#     self.assertEqual(res.status_code, status.HTTP_200_OK)

#   def test_remove_task_wrong_user(self):
#     res = self.client.get('/selected_task/12')
#     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

#   def test_remove_task_nontaken(self):
#     res = self.client.get('/selected_task/12')
#     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from channels.testing import WebsocketCommunicator
from tasksystem.asgi import application
from taskselection.models import Task
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import pytest

"""
To run this test case to test WebSockets for production, you'll to install
pytest and pytest-asyncio:

pip install pytest pytest-asyncio
"""

class TaskSelectionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        Task.objects.create(desc='Test Task 1', code=1, category=1, location='Location 1', date='2023-01-01', starttime='09:00:00', endtime='10:00:00')
        Task.objects.create(desc='Test Task 2', code=2, category=1, location='Location 2', date='2023-01-01', starttime='10:00:00', endtime='11:00:00')

    def test_list_available_tasks(self):
        # Create some available tasks
        Task.objects.create(desc='Available Task 1', code=101, category=1, location='Location 1', date='2023-01-01', starttime='09:00:00', endtime='10:00:00')
        Task.objects.create(desc='Available Task 2', code=102, category=1, location='Location 2', date='2023-01-01', starttime='10:00:00', endtime='11:00:00')
        
        url = reverse('available-tasks')  # Make sure you have this name in your urls.py
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreater(len(res.data), 0)
        print(f"Number of available tasks: {len(res.data)}")  # Add this line for debugging

    def test_list_user_tasks(self):
        res = self.client.get('/selected_tasks/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_accept_task_available(self):
        res = self.client.put('/select_task/1')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_accept_task_unavailable(self):
       # First, let's create a task and assign it to another user
       other_user = User.objects.create_user(username='otheruser', password='12345')
       task = Task.objects.create(desc='Unavailable Task', code=999, category=1, location='Location', date='2023-01-01', starttime='09:00:00', endtime='10:00:00', sv=other_user)
       
       # Now try to accept this task
       res = self.client.put(f'/select_task/{task.code}')
       self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_task_success(self):
        self.client.put('/select_task/2')
        res = self.client.delete('/select_task/2')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_remove_task_wrong_user(self):
        other_user = User.objects.create_user(username='otheruser', password='12345')
        task = Task.objects.create(desc='Other Task', code=3, category=1, location='Location 3', date='2023-01-01', starttime='11:00:00', endtime='12:00:00', sv=other_user)
        res = self.client.delete(f'/select_task/{task.code}')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_task_nontaken(self):
        res = self.client.delete('/select_task/1')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_websocket_connection():
    communicator = WebsocketCommunicator(application, "/ws/tasks/")
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()




@pytest.mark.django_db
def test_channel_layer():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_add)("test_group", "test_channel")
    async_to_sync(channel_layer.group_send)(
        "test_group", {"type": "test.message", "text": "hello"}
    )

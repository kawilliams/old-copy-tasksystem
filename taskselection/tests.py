from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

# class LoginTestCase(TestCase):
  # def test_login_success(self):
    # pass
  # def test_login_failure(self):
    # pass
  # def test_logout(self):
    # pass

class TaskSelectionTestCase(APITestCase):
  def test_list_available_tasks(self):
    res = self.client.get('/available_tasks')
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(len(res.data), 4)

  def test_list_user_tasks(self):
    res = self.client.get('/selected_tasks')
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(len(res.data), 2)

  def test_accept_task_available(self):
    res = self.client.get('/selected_task/3')
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(len(res.data), 2)

  def test_accept_task_unavailable(self):
    res = self.client.get('/selected_task/12')
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_remove_task_success(self):
    res = self.client.get('/selected_task/9')
    self.assertEqual(res.status_code, status.HTTP_200_OK)

  def test_remove_task_wrong_user(self):
    res = self.client.get('/selected_task/12')
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_remove_task_nontaken(self):
    res = self.client.get('/selected_task/12')
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



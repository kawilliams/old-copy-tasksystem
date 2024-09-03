from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from taskselection.models import Task
from taskselection.serializers import TaskSerializer
from rest_framework.views import APIView
from channels import Group
import json

class AvailableTaskList(APIView):
  def get(self, request):
    tasks = Task.objects.filter(sv=None)
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)

class SelectedTaskList(APIView):
  def get(self, request):
    sv = request.user
    #sv = User.objects.get(pk=1)
    tasks = Task.objects.filter(sv=sv)
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)

class SelectTask(APIView):
  def put(self, request, code):
    sv = request.user
    #sv = User.objects.get(pk=1)
    task = Task.objects.get(code=code)
    if task.sv == None:
      task.sv = sv
      task.save()
      serializer = TaskSerializer(task)
      Group('task_selections').send({
        'text': json.dumps({'action': 'remove', 'task': serializer.data})
      })
      return JsonResponse(serializer.data, safe=False)
    else:
      return Response({"code": "task_taken"}, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, code):
    sv = request.user
    #sv = User.objects.get(pk=1)
    task = Task.objects.get(code=code)
    if task.is_sticky:
      return Response({"code": "task_not_removable"}, status=status.HTTP_400_BAD_REQUEST)
    elif task.sv == sv:
      task.sv = None
      task.save()
      serializer = TaskSerializer(task)
      Group('task_selections').send({
        'text': json.dumps({'action': 'add', 'task': serializer.data})
      })
      return JsonResponse(serializer.data, safe=False)
    else:
      return Response({"code": "not_your_task"}, status=status.HTTP_400_BAD_REQUEST)


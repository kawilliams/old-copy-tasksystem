#taskselection/views.py
# from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from taskselection.models import Task
from taskselection.serializers import TaskSerializer, UserSerializer
from taskselection.permissions import IsOwnerOrReadOnly
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view

######## Used to test message passing through Channels #####
from django.shortcuts import render

def index(request):
    return render(request, "taskselection/index.html")

def room(request, room_name):
    return render(request, "taskselection/room.html", {"room_name": room_name})
######## END testing message passing through Channels #####


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'available_tasks': reverse('available-tasks', request=request, format=format),
        'selected_tasks': reverse('selected-tasks', request=request, format=format)
    })

class AvailableTaskList(generics.ListAPIView):
  #@sync_to_async 
  queryset = Task.objects.filter(sv__isnull=True)
  serializer_class = TaskSerializer
  permission_classes = [permissions.IsAuthenticated]


class SelectedTaskList(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(sv=self.request.user)

class SelectTask(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'code'

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TaskHighlight(generics.GenericAPIView):
    queryset = Task.objects.all()
    render_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        return Response(task.desc)

# class SelectedTaskList(generics.ListAPIView):
#   def get(self, request):
#     sv = request.user
#     tasks = Task.objects.filter(sv=sv)
#     serializer = TaskSerializer(tasks, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

"""
# SnippetDetail
class SelectTask(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # def put(self, request, code):
    #     sv = request.user
    #     try:
    #         task = Task.objects.get(code=code)
    #     except Task.DoesNotExist:
    #         return Response({"code": "task_not_found"}, status=status.HTTP_404_NOT_FOUND)
        
    #     if task.sv is None:
    #         task.sv = sv
    #         task.save()
    #         serializer = TaskSerializer(task)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response({"code": "task_taken"}, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, code):
    #     sv = request.user
    #     try:
    #         task = Task.objects.get(code=code)
    #     except Task.DoesNotExist:
    #         return Response({"code": "task_not_found"}, status=status.HTTP_404_NOT_FOUND)
        
    #     if task.is_sticky:
    #         return Response({"code": "task_not_removable"}, status=status.HTTP_400_BAD_REQUEST)
    #     elif task.sv == sv:
    #         task.sv = None
    #         task.save()
    #         serializer = TaskSerializer(task)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response({"code": "not_your_task"}, status=status.HTTP_400_BAD_REQUEST)
    #         """
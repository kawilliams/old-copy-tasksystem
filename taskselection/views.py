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


# from django.shortcuts import render

# def index(request):
#     return render(request, "taskselection/index.html")

# def room(request, room_name):
#     return render(request, "taskselection/room.html", {"room_name": room_name})

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'tasks': reverse('task-list', request=request, format=format)
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# SnippetList
class TaskViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides 'list', 'create',
    'retrieve', 'update', and 'destroy' actions.

    Additionally, we also provide an extra 'highlight' action.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        task = self.get_object()
        return Response(task.desc)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AvailableTaskList(generics.ListCreateAPIView):
  #@sync_to_async 
  queryset = Task.objects.all()
  serializer_class = TaskSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  def perform_create(self, serializer):
    serializer.save(sv=self.request.user)

# class SelectedTaskList(generics.ListAPIView):
#   def get(self, request):
#     sv = request.user
#     tasks = Task.objects.filter(sv=sv)
#     serializer = TaskSerializer(tasks, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# SnippetDetail
class SelectTask(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


#SnippetHighlight
class TaskHighlight(generics.GenericAPIView):
    queryset = Task.objects.all()
    render_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        return Response(task.desc)
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
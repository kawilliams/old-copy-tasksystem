#taskselection/serializers.py
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers, routers, viewsets
from taskselection.models import Task

class TaskSerializer(serializers.HyperlinkedModelSerializer):
  sv = serializers.ReadOnlyField(source='sv.username')
  highlight = serializers.HyperlinkedIdentityField(view_name='task-highlight', format='html')

  class Meta:
    model = Task
    fields = ['url', 'id', 'highlight', 'desc', 'code', 'category', 'location', 
              'date', 'starttime', 'endtime','is_sticky', 'sv']

class UserSerializer(serializers.HyperlinkedModelSerializer):
  tasks = serializers.HyperlinkedRelatedField(many=True, view_name='task-detail', read_only=True)#queryset=Task.objects.all())

  class Meta:
    model = User
    fields = ['url', 'id', 'username', 'tasks']

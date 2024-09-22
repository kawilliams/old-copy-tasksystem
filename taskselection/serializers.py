#taskselection/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from taskselection.models import Task

class TaskSerializer(serializers.HyperlinkedModelSerializer):
  sv = serializers.ReadOnlyField(source='sv.username')
  highlight = serializers.HyperlinkedIdentityField(
    view_name='task-highlight', 
    format='html', 
    lookup_field='code'
    )

  class Meta:
    model = Task
    fields = ['url', 'id', 'highlight', 'desc', 'code', 'category', 'location', 
              'date', 'starttime', 'endtime','is_sticky', 'sv']
    extra_kwargs = {
        'url': {'view_name': 'task-detail', 'lookup_field': 'code'}
    }

class UserSerializer(serializers.HyperlinkedModelSerializer):
  tasks = serializers.HyperlinkedRelatedField(
    many=True, 
    view_name='task-detail', 
    lookup_field='code', 
    read_only=True)

  class Meta:
    model = User
    fields = ['url', 'id', 'username', 'tasks']

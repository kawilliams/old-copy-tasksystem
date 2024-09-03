from django.contrib.auth.models import User, Group
from rest_framework import serializers
from taskselection.models import Task

class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = ('desc', 'code', 'category', 'location', 
              'date', 'starttime', 'endtime','is_sticky')


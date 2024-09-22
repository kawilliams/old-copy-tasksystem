#taskselection/models.py
from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings


class Task(models.Model):
    desc = models.TextField()
    location = models.TextField()
    code = models.IntegerField(unique=True)
    date = models.DateField()
    starttime = models.TimeField()
    endtime = models.TimeField()
    _is_sticky = models.BooleanField(default=False, db_column="is_sticky")
    sv = models.ForeignKey('auth.User', null=True, related_name='tasks', on_delete=models.SET_NULL) #(User, null=True, on_delete=models.SET_NULL)
    category = models.IntegerField(default=0)

    @property
    def is_sticky(self):
        if settings.LOCK_TASKSELECTION:
            return True
        else:
            return self._is_sticky

    @is_sticky.setter
    def is_sticky(self, value):
        self._is_sticky = value

    class Meta:
        ordering = ['code']
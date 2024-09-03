from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from taskselection.models import Task
import sys
import csv
from tasksystem.settings.base import *

User = get_user_model()

EXPORT_FIELDS = [
  'desc',
  'code',
  'date',
  'starttime',
  'endtime',
  'location',
  'firstname',
  'lastname',
  'email'
]

class Command(BaseCommand):
  help = 'Creates new tasks in the db for the given csv file'

  def add_arguments(self, parser):
    parser.add_argument('tasks', type=str)

  def handle(self, *args, **options):
    with open(options['tasks'], 'w') as csvfile:
      csvwriter = csv.writer(csvfile, delimiter=';')
      csvwriter.writerow(EXPORT_FIELDS)
      # if this doesn't work the delimiter might be wrong
      tasks = Task.objects.all()
      print("exporting...")
      print(BASE_DIR);
      #.values_list(EXPORT_FIELDS, flat=True)
      for task in tasks:
        row = [task.desc, task.code, task.date, task.starttime, task.endtime,  task.location]
        if task.sv:
          row = row + [task.sv.first_name, task.sv.last_name, task.sv.email]
        csvwriter.writerow(row)
        values = [str(x) for x in row]
        print(";".join(values))

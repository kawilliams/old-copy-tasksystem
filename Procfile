release: python manage.py migrate --settings=tasksystem.settings.prod
   web: daphne -b 0.0.0.0 -p $PORT  tasksystem.asgi:application
   worker: python manage.py runworker --settings=tasksystem.settings.prod -v2
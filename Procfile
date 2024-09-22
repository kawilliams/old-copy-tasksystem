release: python manage.py migrate --settings=tasksystem.settings.prod
   web: daphne -b 0.0.0.0 -p 8000 tasksystem.asgi:application
   worker: python manage.py runworker -v2
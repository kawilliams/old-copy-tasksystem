import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tasksystem.settings.prod')
django.setup()

from django.db import connections
from django.db.utils import OperationalError

db_conn = connections['default']
try:
    c = db_conn.cursor()
    print("Successfully connected to the database.")
except OperationalError:
    print("Failed to connect to the database.")
from tasksystem.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Option to lock down the task system
# LOCK_TASKSELECTION = False
if os.environ.get('LOCK_TASKS', 'false').lower() == 'true':
    LOCK_TASKSELECTION = True
else:
    LOCK_TASKSELECTION = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p#$hm-6n0^c6f6iuf0^iu0sla_()$)gt196m=cz&6_48_=68yq'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

CHANNEL_LAYERS['default'] = {
    "BACKEND": "asgiref.inmemory.ChannelLayer",
    "ROUTING": "taskselection.routing.channel_routing",
}

# CORS settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_REPLACE_HTTPS_REFERER = True
CORS_ALLOW_CREDENTIALS = True

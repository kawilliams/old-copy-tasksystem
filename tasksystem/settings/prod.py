from tasksystem.settings.base import *
import dj_database_url
import os
from urllib.parse import urlparse

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Option to lock down the task system
if os.environ.get('LOCK_TASKS', 'false').lower() == 'true':
    LOCK_TASKSELECTION = True
else:
    LOCK_TASKSELECTION = False


# Use a postgres database for production, to match Heroku.
# Username: tasksystem_user, Password: 070625
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://tasksystem_user:070625@localhost:5432/tasksystem_db',
        conn_max_age=600
    )
}

if DATABASES['default'] == {}:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
# DATABASES = {
#     'default' : {
#     'ENGINE': 'django.db.backends.mysql',
#     'NAME': 'vissv_db',
#     'USER': 'visweeksvchairs',
#     'PASSWORD': 'SVs@visweek2023',
#     'ATOMIC_REQUESTS': True,
#     'HOST': '127.0.0.1',
#     'PORT': '3306',
#     }
# }


ALLOWED_HOSTS = ['old-copy-tasksystem.herokuapp.com', 'https://old-copy-tasksystem-9f16a052b963.herokuapp.com/', 'localhost', '127.0.0.1']

# websockets
redis_url = urlparse(os.environ.get('REDIS_URL', 'redis://localhost:6379'))
CHANNEL_LAYERS['default'] = {
    "BACKEND": "channels_redis.core.RedisChannelLayer",
    "CONFIG": {
        "hosts": [(redis_url.hostname, redis_url.port)],
    },
    #"ROUTING": "taskselection.routing.channel_routing", #No longer needed?
}

SECRET_KEY = os.environ['SECRET_KEY']
#SECRET_KEY = os.environ.get('SECRET_KEY')

# CORS settings
#CORS_ORIGIN_ALLOW_ALL = True
#CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = ['http://vissv.org', 'https://old-copy-tasksystem.herokuapp.com', 'http://localhost', 'http://127.0.0.1', 'http://54.201.77.132', 'http://159.127.104.69']
                        
CORS_ALLOW_CREDENTIALS = True

# Daphne
ASGI_APPLICATION = 'tasksystem.asgi.application'

# Configure static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',  # You can change this path as needed
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
        },
        'channels': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
        },
    },
}
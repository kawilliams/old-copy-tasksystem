
# server interface for websockets

import os
from channels.layers import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasksystem.settings")
channel_layer = get_channel_layer()


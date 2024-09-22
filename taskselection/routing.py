#taskselection/routing.py
# websocket "urls"

# from . import consumers

# channel_routing = {
#   'websocket.connect': consumers.ws_connect,
#   'websocket.receive': consumers.ws_receive,
#   'websocket.disconnect': consumers.ws_disconnect,
# }

from django.urls import re_path, path, include
from . import consumers

websocket_urlpatterns = [
    #re_path(r'ws/task_selections/$', consumers.TaskSelectionConsumer.as_asgi()),
    #path('', include(router.urls)),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.TaskSelectionConsumer.as_asgi()),
]
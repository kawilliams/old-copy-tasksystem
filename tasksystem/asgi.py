
# server interface for websockets
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tasksystem.settings.dev') #change to prod for production

django_asgi_application = get_asgi_application()

from taskselection.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
    "http": django_asgi_application,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(
            websocket_urlpatterns
        ))
    ),
}
)
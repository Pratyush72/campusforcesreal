import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import realtime_chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusforce.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            realtime_chat.routing.websocket_urlpatterns
        )
    ),
})

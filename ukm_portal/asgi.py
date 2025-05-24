import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import mahasiswa.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ukm_portal.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            mahasiswa.routing.websocket_urlpatterns
        )
    ),
})
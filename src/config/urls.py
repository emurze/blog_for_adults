from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.blog.urls', namespace='blog')),
]

if settings.DEBUG:
    urlpatterns += [
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        path('__debug__/', include('debug_toolbar.urls'))
    ]
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    allowed_ips = ["127.0.0.1", "10.0.2.2"]
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + allowed_ips

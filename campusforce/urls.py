from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Connect core app routes
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # ✅ Link accounts app
]


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # agar core hai
    path('accounts/', include('accounts.urls')),  # ✅ Ye line jaruri hai
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # 👈 ye line
]
from django.shortcuts import redirect
from core import views as core_views  # Import core_views

from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('accounts/', include('accounts.urls')),
#     path('', core_views.homepage, name='homepage'),  # 👈 homepage route
# ]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),        # Home + dashboard etc.
    path('accounts/', include('accounts.urls')),  # Login/signup/logout
]
# campusforce/urls.py
from django.contrib import admin
from django.urls import path, include
from core import views  # <- yaha se views aa rha hai

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('members/', include('Member.urls')),
        # Your accounts app URLs
    
        # Include gallery app URLs
    #path('', include('core.urls')),               # Your core app URLs (home, etc.)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

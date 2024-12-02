from django.contrib import admin
from django.urls import path, include
from demoapp.views import home, about, contact
from django.conf import settings
from django.conf.urls.static import static

# Define the URL patterns for the project
urlpatterns = [
    path('', include('demoapp.urls')),  # Include URLs from the 'demoapp' application
    path('admin/', admin.site.urls),  # Admin site URL
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

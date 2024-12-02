from django.urls import path
from django.contrib import admin
from .views import home, about, contact  # Import view functions
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # URL pattern for the admin site
    path('', home, name='home'),  # URL pattern for the home page
    path('about/', about, name='about'),  # URL pattern for the about page
    path('contact/', contact, name='contact'),  # URL pattern for the contact page
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Serve static files in debug mode

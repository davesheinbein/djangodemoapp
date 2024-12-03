from django.contrib import admin
from django.urls import path, include
from demoapp.views import home, about, contact, register
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Define the URL patterns for the project
urlpatterns = [
    path('', include('demoapp.urls')),  # Include URLs from the 'demoapp' application
    path('admin/', admin.site.urls),  # Admin site URL
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Login page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout page
    path('register/', register, name='register'),  # Register page
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

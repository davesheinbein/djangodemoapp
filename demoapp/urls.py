from django.urls import path, include
from django.contrib import admin
from . import views  # Import views module
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from .views import error_404_view, register, admin_view, home, about, contact, visitors, edit_visitor, update_visitor, delete_visitor

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('admin/', admin.site.urls),  # URL pattern for the admin site
    path('admin_view/', admin_view, name='admin_view'),  # Admin-specific view
    path('about/', about, name='about'),  # About page
    path('contact/', contact, name='contact'),  # Contact page
    path('visitors/', visitors, name='visitors'),  # Visitors page
    path('visitors/update/<int:visitor_id>/', update_visitor, name='update_visitor'),  # Update visitor
    path('visitors/delete/<int:visitor_id>/', delete_visitor, name='delete_visitor'),  # Delete visitor
    path('visitors/edit/<int:visitor_id>/', edit_visitor, name='edit_visitor'),  # Edit visitor
    path('register/', register, name='register'),  # Register page
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Serve static files in debug mode

handler404 = error_404_view

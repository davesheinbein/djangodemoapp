from django.contrib import admin
from django.urls import path, include, re_path
from demoapp.views import register, CustomLoginView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Define the URL patterns for the project
urlpatterns = [
    path('', include('demoapp.urls')),  # Include URLs from the 'demoapp' application
    # path('admin/', admin.site.urls),  # Admin site URL
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),  # Use custom login view
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Logout page with redirect to home
    path('register/', register, name='register'),  # Register page
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path, include
from django.contrib import admin
from . import views  # Import views module
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from .views import error_404_view, register, admin_view, home, about, contact, visitors, edit_visitor, update_visitor, delete_visitor, CustomLoginView, ajax_edit_visitor, ajax_delete_visitor, ajax_update_visitor, practice, edit_profile, add_article, delete_tag, add_category, delete_article, update_profile, add_profile, add_tag, add_author, add_book, delete_profile  # Import the practice view

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
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('ajax/visitors/edit/<int:visitor_id>/', ajax_edit_visitor, name='ajax_edit_visitor'),
    path('ajax/visitors/delete/<int:visitor_id>/', ajax_delete_visitor, name='ajax_delete_visitor'),
    path('ajax/visitors/update/<int:visitor_id>/', ajax_update_visitor, name='ajax_update_visitor'),
    path('practice/', practice, name='practice'),  # Add URL pattern for practice page
    path('practice/edit_profile/<int:profile_id>/', edit_profile, name='edit_profile'),
    path('practice/add_article/', add_article, name='add_article'),
    path('practice/delete_tag/<int:tag_id>/', delete_tag, name='delete_tag'),
    path('practice/add_category/', add_category, name='add_category'),
    path('practice/delete_article/<int:article_id>/', delete_article, name='delete_article'),
    path('practice/update_profile/<int:profile_id>/', update_profile, name='update_profile'),
    path('practice/add_profile/', add_profile, name='add_profile'),
    path('practice/add_tag/', add_tag, name='add_tag'),
    path('practice/add_author/', add_author, name='add_author'),
    path('practice/add_book/', add_book, name='add_book'),
    path('practice/delete_profile/<int:profile_id>/', delete_profile, name='delete_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Serve static files in debug mode

handler404 = error_404_view

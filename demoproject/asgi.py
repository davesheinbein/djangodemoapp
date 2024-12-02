"""
ASGI config for demoapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default settings module for the 'demoproject'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demoproject.settings')

# Get the ASGI application for the project
application = get_asgi_application()

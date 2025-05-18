"""
ASGI config for core_project_name project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# TODO: Replace 'core_project_name.settings' with the actual project settings path
# This will be dynamically updated by the initialize_new_project.py script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_project_name.settings')

application = get_asgi_application()
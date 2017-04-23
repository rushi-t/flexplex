"""
WSGI config for flexplex project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""
import os
import sys
sys.path.append('/opt/bitnami/apps/django/django_projects/flexplex')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/flexplex/egg_cache")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flexplex.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

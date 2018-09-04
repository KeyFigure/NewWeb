"""
WSGI config for NewWeb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#作为项目的运行在 WSGI 兼容的Web服务器上的入口

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewWeb.settings')

application = get_wsgi_application()

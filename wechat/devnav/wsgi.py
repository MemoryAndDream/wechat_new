#coding=utf8
"""
WSGI config for devnav project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from os.path import join,dirname,abspath
import sys
#wsgi是运行在embeded的模式下，即在apache的worker进程内。对wsgi application的修改，需要重启apache才能生效
PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = "devnav.settings"#这里不要用默认的，不然多个项目部署会互相影响!!

application = get_wsgi_application()

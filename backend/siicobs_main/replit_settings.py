"""Configuración de desarrollo aislada para la vista previa de Replit."""
import os

from .settings import *

SECRET_KEY = os.environ['SESSION_SECRET']
DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'replit.sqlite3'),
    }
}
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MIDDLEWARE = [
    middleware for middleware in MIDDLEWARE
    if middleware != 'whitenoise.middleware.WhiteNoiseMiddleware'
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    directory for directory in STATICFILES_DIRS if os.path.isdir(directory)
]
CSRF_TRUSTED_ORIGINS = [
    'https://' + domain
    for domain in os.environ.get('REPLIT_DOMAINS', '').split(',')
    if domain
]

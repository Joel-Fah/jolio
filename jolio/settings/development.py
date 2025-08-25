# Local development settings for Jolio
import dj_database_url
from dotenv import load_dotenv

from .base import *

# Load prod env file
load_dotenv(
    os.path.join(BASE_DIR, 'dev.env')
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p(h^s8-1g15w$)z4wza90i2c9h53=*lbq!m*!h%3*e&8-pxty!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS += ['django_browser_reload']

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'supabase': dj_database_url.parse(os.getenv('SUPABASE_POSTGRESQL_URL')),
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'theme/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR / 'media/')

# Whitenoise settings
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "LOCATION": MEDIA_ROOT,
    },
}

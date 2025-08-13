# Production settings for Jolio
from .base import *
from dotenv import load_dotenv

# Load prod env file
load_dotenv(
    os.path.join(BASE_DIR, 'prod.env')
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv("DEBUG", False) == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(" ") if os.getenv('ALLOWED_HOSTS') else []

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    # Configure a database for your production environment
}

SITE_URL = os.getenv('SITE_URL')

# Storage settings
# Configure your storage settings for production

# Static and Media files
# Configure your static and media files for production

# STORAGES = {}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
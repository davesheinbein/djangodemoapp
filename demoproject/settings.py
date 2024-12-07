"""
Django settings for demoapp project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p%f(-5j%fos#r_b9*w1kmjftw$!oo9(d%fv0#w1_ya-#q_+$%i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Define the allowed hosts for the project
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',  # Admin site
    'django.contrib.auth',  # Authentication framework
    'django.contrib.contenttypes',  # Content types framework
    'django.contrib.sessions',  # Session framework
    'django.contrib.messages',  # Messaging framework
    'django.contrib.staticfiles',  # Static files framework
    'demoapp',  # Custom application
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'livereload',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Security middleware
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session middleware
    'django.middleware.common.CommonMiddleware',  # Common middleware
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication middleware
    'django.contrib.messages.middleware.MessageMiddleware',  # Messaging middleware
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection middleware
    'allauth.account.middleware.AccountMiddleware',
]

# Root URL configuration
ROOT_URLCONF = 'demoproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Template backend
        'DIRS': [BASE_DIR / 'templates'],  # Directories to search for templates
        'APP_DIRS': True,  # Enable template loading from installed apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Debug context processor
                'django.template.context_processors.request',  # Request context processor
                'django.contrib.auth.context_processors.auth',  # Authentication context processor
                'django.contrib.messages.context_processors.messages',  # Messaging context processor
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'demoproject.wsgi.application'

# Database configuration
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Database engine
        'NAME': BASE_DIR / 'db.sqlite3',  # Database name
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # User attribute similarity validator
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Minimum length validator
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Common password validator
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Numeric password validator
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'  # Language code
TIME_ZONE = 'UTC'  # Time zone
USE_I18N = True  # Enable internationalization
USE_TZ = True  # Enable time zone support

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = 'static/'  # URL for static files
STATICFILES_DIRS = [
    BASE_DIR / "static/css",  # Directories to search for CSS files
    BASE_DIR / "static/js",   # Directories to search for JS files
    BASE_DIR / "static/images",  # Directories to search for image files
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory to collect static files

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Default primary key field type

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'concise': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',  # ERROR / DEBUG
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'error.log',
            'formatter': 'concise',
        },
        'console': {
            'level': 'ERROR',  # ERROR / DEBUG
            'class': 'logging.StreamHandler',
            'formatter': 'concise',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',  # ERROR / DEBUG
            'propagate': True,
        },
        'demoapp': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',  # ERROR / DEBUG
            'propagate': True,
        },
    },
}

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'  # Redirect to home after logout

SITE_ID = 1

LOGIN_URL = 'login'

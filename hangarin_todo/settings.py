from pathlib import Path
import socket
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-hangarin-todo-midterm-project-secret-key-2024'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Required for Social Login
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # PWA Support
    'pwa',

    'tasks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'hangarin_todo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hangarin_todo.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if "pythonanywhere" in socket.gethostname():
    SITE_ID = 2  # ← pythonanywhere.com
else:
    SITE_ID = 3  # ← 127.0.0.1:8000

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# 1. Allow Django to trust your live domain for CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://hansmaggot.pythonanywhere.com',
]

# 2. Tell Django how to handle cookies behind PythonAnywhere's proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 3. Ensure the logout doesn't require a POST form (Fixes the 403 on Redirect)
ACCOUNT_LOGOUT_ON_GET = True

# 4. Use "Lax" for cookies to allow the Google Redirect to work smoothly
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

SOCIALACCOUNT_ADAPTER = 'tasks.adapter.CorporateOnlyAdapter'
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'select_account', # This fixes the auto-login loop
        },
    }
}

# ── Progressive Web App ──────────────────────────────────────────────────────
PWA_APP_NAME = 'Hangarin'
PWA_APP_DESCRIPTION = 'Hangarin — Your personal task manager. Organize work, track progress, and stay on top of everything.'
PWA_APP_THEME_COLOR = '#0f0f0f'
PWA_APP_BACKGROUND_COLOR = '#f0f0ec'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'portrait-primary'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_DISPLAY_READY_PROMPT = True
PWA_APP_ICONS = [
    {
        'src': '/static/img/icon-192.png',
        'sizes': '192x192',
        'type': 'image/png',
        'purpose': 'any maskable' # This makes it look like a real app icon
    },
    {
        'src': '/static/img/icon-512.png',
        'sizes': '512x512',
        'type': 'image/png',
        'purpose': 'any maskable'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/img/icon-192.png',
        'sizes': '192x192',
        'type': 'image/png'
    },
    {
        'src': '/static/img/icon-512.png',
        'sizes': '512x512',
        'type': 'image/png'
    }
]
PWA_APP_SCREENSHOTS = [
    {
        'src': '/static/img/screenshot-mobile.png', # Ensure this file exists in static/img/
        'sizes': '750x1334',
        'type': 'image/png',
        'form_factor': 'narrow',
    },
    {
        'src': '/static/img/screenshot-desktop.png', # Ensure this file exists in static/img/
        'sizes': '1280x720',
        'type': 'image/png',
        'form_factor': 'wide',
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-us'
PWA_APP_CATEGORIES = ['productivity']
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static', 'serviceworker.js')
PWA_SERVICE_WORKER_TIMEOUT = 1000
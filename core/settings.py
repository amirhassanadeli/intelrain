import os
from datetime import timedelta
from pathlib import Path

import environ

# ---------------------------------------------------------
# Base Directory
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------
# Environment Variables
# ---------------------------------------------------------
env = environ.Env(
    DEBUG=(bool, False),
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

ENV = env("ENV", default="local")

# سپس فایل مخصوص env را بخوان
environ.Env.read_env(
    os.path.join(BASE_DIR, f'.env.{ENV}')
)
# ---------------------------------------------------------
# Security
# ---------------------------------------------------------
SECRET_KEY = env("SECRET_KEY", default="django-insecure-ci-key")

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1"])
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ---------------------------------------------------------
# Custom Variables
# ---------------------------------------------------------
KAVENEGAR_API_KEY = env("KAVENEGAR_API_KEY", default="")

# ---------------------------------------------------------
# Applications
# ---------------------------------------------------------
INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',

    # Local Apps
    'services',
    'portfolio',
    'contacts',
]

# ---------------------------------------------------------
# Middleware
# ---------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------------------------------------
# URLs & WSGI
# ---------------------------------------------------------
ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

# ---------------------------------------------------------
# Templates
# ---------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ---------------------------------------------------------
# Database
# ---------------------------------------------------------
if ENV == "server":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',

            'NAME': env('DB_NAME'),

            'USER': env('DB_USER'),

            'PASSWORD': env('DB_PASSWORD'),

            'HOST': env('DB_HOST'),

            'PORT': env('DB_PORT'),
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',

            'NAME': BASE_DIR / env(
                'SQLITE_NAME',
                default='db.sqlite3'
            ),
        }
    }

# ---------------------------------------------------------
# REST Framework
# ---------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# ---------------------------------------------------------
# JWT
# ---------------------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),

    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    'ROTATE_REFRESH_TOKENS': True,

    'BLACKLIST_AFTER_ROTATION': True,

    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',

    'SIGNING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ---------------------------------------------------------
# Password Validation
# ---------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ---------------------------------------------------------
# Internationalization
# ---------------------------------------------------------
LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

# ---------------------------------------------------------
# Static & Media Files
# ---------------------------------------------------------

if ENV == "server":
    STATIC_URL = '/static/'
    STATIC_ROOT = '/var/www/intelrain/static/'

    MEDIA_URL = '/media/'
    MEDIA_ROOT = '/var/www/intelrain/media/'
    
else:
    
    STATIC_URL = '/static/'

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    )


    MEDIA_URL = '/media/'

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ---------------------------------------------------------
# Default PK
# ---------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
if ENV == "server":
    
    CORS_ALLOW_ALL_ORIGINS = True

    CORS_ALLOWED_ORIGINS = [
        "https://www.intelrain.com",
        "https://intelrain.com",
    ]

    CORS_ALLOW_CREDENTIALS = True

else:
    CORS_ALLOW_ALL_ORIGINS = False

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",

        "http://127.0.0.1:3000",
    ]

    CORS_ALLOW_CREDENTIALS = True

# ---------------------------------------------------------
# Security Settings (Production)
# ---------------------------------------------------------
if ENV == "server":

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = 'DENY'

# ---------------------------------------------------------
# Redis (Celery or Cache)
# ---------------------------------------------------------
REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/0")
        
# ---------------------------------------------------------
# Email
# ---------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = env("EMAIL_HOST", default="localhost")
EMAIL_PORT = env.int("EMAIL_PORT", default=25)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)

EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")

# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------
LOG_DIR = os.path.join(BASE_DIR, 'logs')

os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,

    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': (
                '%(asctime)s '
                '%(levelname)s '
                '%(module)s '
                '%(message)s'
            )
        },

        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'handlers': {
        'file': {
            'level': 'INFO',

            'class': 'logging.FileHandler',

            'filename': os.path.join(
                LOG_DIR,
                'django.log'
            ),

            'formatter': 'verbose',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['file'],

            'level': 'INFO',

            'propagate': True,
        },
    },
}
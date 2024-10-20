
import os

from config.env import APPS_DIR, BASE_DIR, env

env.read_env(os.path.join(BASE_DIR, ".env"))

import pymysql

pymysql.install_as_MySQLdb()

SECRET_KEY = 'django-insecure-1q6v^%d6sq$h*p9o+_*px93+z83*lb1^)f$xe&&%flgwt7eqhi'

DEBUG = env.bool("DJANGO_DEBUG", default=True)

ALLOWED_HOSTS = ["*"]


AUTH_USER_MODEL = "users.BaseUser"


LOCAL_APPS = [
    "royal.core.apps.CoreConfig", 
    "royal.api.apps.ApiConfig",
    "royal.common.apps.CommonConfig",
    "royal.users.apps.UsersConfig",
    "royal.market.apps.MarketConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_jwt",
    "django_filters",
    "corsheaders",
    "django_extensions",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="mysql://test2:0909@localhost:3306/test2"
    ),
}

# Special configuration for GitHub Actions
if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "github_actions",  
            "USER": "root",            
            "PASSWORD": "",          
            "HOST": "127.0.0.1",    
            "PORT": "3306",           
        }
    }

DATABASES["default"]["ATOMIC_REQUESTS"] = True



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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



# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = "/static/"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "royal.api.exception_handlers.custome_error_handler",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_AUTHENTICATION_CLASSES": [],
}

APP_DOMAIN = env("APP_DOMAIN", default="http://localhost:8000")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



from config.settings.cors import *  

from config.settings.jwt import *  

from config.settings.sessions import *  



"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from environs import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env.bool("DEBUG", default=False)
#
# ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # local
    "apps.bot",
    "apps.staff",
    "apps.checking",
    "api",
    "jobs",

    # lib
    "environs",
    'telegram',
    'rest_framework',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'template'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static2")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#  variables
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = ["*"]
DATABASES = {'default': env.dj_db_url('DATABASE_URL')}
SECRET_KEY = env.str('SECRET_KEY')
TELEGRAM_TOKEN = env.str('TELEGRAM_TOKEN')
S_TOKEN = env.str('S_TOKEN')
URL_1C = env.str('URL_1C')
LOGIN_1C = env.str('LOGIN_1C')
PASSWORD_1C = env.str('PASSWORD_C')
ALLOWED_IPS = env.list('ALLOWED_IPS')
SEND_CHECKING_ID = env.str('SEND_CHECKING_ID')
WORKING_TIME = env.str('WORKING_TIME')

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Radius Intranet Admin",
    #
    # # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Admin",
    #
    # # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Intranet",
    #
    # # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": r'Radius_Mobile.png',

    # # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    # "login_logo": r'logo\logo.png',
    #
    # # Logo to use for login form in dark themes (defaults to login_logo)
    # "login_logo_dark": None,
    #
    # # CSS classes that are applied to the logo above
    # "site_logo_classes": "img-circle",
    #
    # # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    #
    # # Welcome text on the login screen
    "welcome_sign": "Intranet Admin panel",
    #
    # # Copyright on the footer
    "copyright": "radius.uz",
    #
    # # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "staff.Total",
    #
    # # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": 'photo',
    #
    # ############
    # # Top Menu #
    # ############
    #
    # # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        # {"name": "Дашбоард", "url": "dashboard", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "staff.workers", "permissions": ["staff.view_workers"]},
        {"model": "staff.Total", "permissions": ["staff.view_total"]},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        # {"app": "staff", "icon": "fas fa-users", "models": ("staff.Total",)},
    ],

    # # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["staff.total", "staff.salarys", "staff.leave", "staff.bonus", "staff.request_price",
                              "staff.workers", "staff.department", "staff.inftech", "staff.ITRequestPrice",
                              "staff.notification", "staff.totaldepartment", "staff.data",
                              "checking.Timekeeping", "checking.AllowedIPs"],

    "icons": {
        "auth.User": "fas fa-users-cog",
        "staff.workers": "fas fa-user",
        "staff.department": "fas fa-building",  # "fas fa-envelope"
        "staff.Salarys": "fas fa-money-bill-wave",
        "staff.bonus": "fas fa-comment-dollar",
        "staff.leave": "fas fa-money-bill-alt",
        "staff.total": "fas fa-chart-pie",
        "staff.request_price": "far fa-clock",
        "staff.inftech": "fas fa-user-tie",
        "staff.ITRequestPrice": "fas fa-clock",
        "staff.Notification": "fas fa-sms",
        "staff.TotalDepartment": "fas fa-university",
        "checking.Timekeeping": "far fa-calendar-alt"

    },
}

try:
    from .local_settings import *
except ImportError:
    pass

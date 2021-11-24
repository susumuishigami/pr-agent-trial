"""
Django settings for maidnomadweb project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from os import environ
from pathlib import Path
from typing import Any


def env_bool(name):
    return environ.get(name) == "True"


def env_str_list(name):
    envval = environ.get(name)
    if not envval:
        return []
    return envval.split(",")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_bool("DJANGO_DEBUG")

ALLOWED_HOSTS = env_str_list("DJANGO_ALLOWED_HOSTS")
SITE_ROOT_URL = environ.get("SITE_ROOT_URL")
SITE_ROOT_TITLE = "メイドカフェでノマド会公式サイト"
SITE_ROOT_DESCRIPTION = "メイドカフェでノマドワークの素晴らしさを世の中に広げる活動をしています。"
SITE_ADSENSE_TRACKING_ID = environ.get("SITE_ADSENSE_TRACKING_ID")
SITE_ADSENSE_CLIENT = environ.get("SITE_ADSENSE_CLIENT")
SITE_ADSENSE_SLOT_BOX = environ.get("SITE_ADSENSE_SLOT_BOX")
SITE_ADSENSE_SLOT_SIDE = environ.get("SITE_ADSENSE_SLOT_SIDE")
SITE_AMAZON_ASSOCIATE_TRACKING_ID = environ.get("SITE_AMAZON_ASSOCIATE_TRACKING_ID")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "admin_ordering",
    "reversion",
    "import_export",
    "mdeditor",
    "apps.core",
    "apps.staticpage",
    "apps.maidlist",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "maidnomadweb.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_common_variables",
            ],
            "builtins": ["apps.core.templatetags.markdowntag"],
        },
    },
]

WSGI_APPLICATION = "maidnomadweb.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "ja-JP"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_L10N = True

USE_TZ = True

X_FRAME_OPTIONS = "SAMEORIGIN"


MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "static/"

# AWS Storage
AWS_S3_ACCESS_KEY_ID = environ.get("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = environ.get("AWS_S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = environ.get("AWS_S3_CUSTOM_DOMAIN")
AWS_LOCATION = "static"

if AWS_S3_ACCESS_KEY_ID and AWS_S3_SECRET_ACCESS_KEY:
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    # AWS の設定をしたら、storageをS3に切り替える
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
    DEFAULT_FILE_STORAGE = "apps.core.backends.MediaStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# MDEDITOR

MDEDITOR_CONFIGS = {
    "default": {
        "language": "en",
        "toolbar": [
            # fmt: off
            "undo", "redo", "|",
            "bold", "del", "italic", "quote", "uppercase", "lowercase", "|",
            "list-ul", "list-ol", "hr", "|",
            "link", "code", "table",
            "|",
            "help", "info",
            "||", "preview", "watch"
        ],
    }
}

# Logging
LOGGING: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": ("%(levelname)s [%(asctime)s] %(name)s %(message)s"),
        },
    },
    "handlers": {
        "console": {
            "level": environ.get("DJANGO_LOG_LEVEL", "DEBUG"),
            "class": "logging.StreamHandler",
            "formatter": "standard",
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "NOTSET",
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

if env_bool("DJANGO_DEBUG_SQL"):
    # DBに発行するSQLログを出力
    LOGGING["loggers"]["django.db.backends"] = {
        "handlers": ["console"],
        "level": "DEBUG",
        "propagate": False,
    }

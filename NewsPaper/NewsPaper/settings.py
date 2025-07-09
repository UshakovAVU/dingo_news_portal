from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-^b48k3u1s728@-1*d8g26_!7*c%ucz$pf9v4r@5s2jx$$53hny'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news',
    'accounts',
    'django_filters',           # Для фильтрации
    'django_extensions',        # Дополнительные инструменты для разработки
    'allauth',                  # Для управления аккаунтами
    'allauth.account',          # Поддержка аккаунта
    'allauth.socialaccount',    # Социальные аккаунты
    'django_apscheduler',       # Планировщик задач
]

# Настройки для django-allauth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Стандартный бэкенд
    'allauth.account.auth_backends.AuthenticationBackend',  # Бэкенд django-allauth
)

SITE_ID = 1  # Не забудь указать ID сайта для allauth

LOGIN_REDIRECT_URL = '/'  # URL после успешного входа
LOGOUT_REDIRECT_URL = '/'  # URL после выхода из системы

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'news', 'templates', 'news'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

WSGI_APPLICATION = 'NewsPaper.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Опционально: настройки для Celery (если используешь)
# CELERY_BROKER_URL = 'redis://localhost:6379/0'  # URL брокера
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
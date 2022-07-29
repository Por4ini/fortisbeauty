from django.conf import global_settings
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
from .local_settings import *
from .configs import *
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATICFILE_DIR  = os.path.join(BASE_DIR, 'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


# Personal data

# try:
#     from .local_settings import *
# except:
#     DEBUG = True
#     # Django secret key
#     SECRET_KEY = ''
#     # New post
#     NEW_POST_KEY = ''
#     # Liw pay
#     LIQPAY_PUBLIC_KEY = ''
#     LIQPAY_PRIVATE_KEY = ''
#     # Gmail
#     GMAIL_ADRESS = ''
#     GMAIL_PASSWORD = ''



ALLOWED_HOSTS = [
    '127.0.0.1', 
    '185.233.36.187',
    'fortisbeauty.store'
]

APPEND_SLASH = True
# Application definition

INSTALLED_APPS = [
    # 'jet.dashboard',
    # 'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'clearcache',
    'ckeditor',
    'ckeditor_uploader',
    'compressor',
    'rest_framework',
    'mptt',
    'django_mptt_admin',
    'django_elasticsearch_dsl',


    'apps.core.apps.CoreConfig',
    'apps.blog.apps.BlogConfig',
    'apps.banners.apps.BannersConfig',
    'apps.shop.apps.ShopConfig',
    'apps.user.apps.UserConfig',
    'apps.order.apps.OrderConfig',
    'apps.main.apps.MainConfig',
    'apps.pages.apps.PagesConfig',
    # 'apps.search.apps.SearchConfig',
    'apps.filters.apps.FiltersConfig',
    'apps.opt.apps.OptConfig',
    'apps.wishlist.apps.WishlistConfig',
    'apps.sync1c.apps.Sync1CConfig',
    'apps.productloader.apps.ProductloaderConfig',
]


SITE_ID = 1


COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

AUTHENTICATION_BACKENDS = [
    'project.auth.UserAuthentication',
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'OPTIONS',
)

IMG_SIZE_S = 480, 480


BOT_TOKEN = '1804134492:AAGQx88cHrWpNShbtgrtUSJQ8Bonfc0dH-s'
BOT_CHATID = '-1001490724377'


MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'project.middleware.metric_middleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.language_change',
                'apps.shop.context_processors.cart',
                'apps.shop.context_processors.categories_tree',
                'apps.user.context_processors.wishlist',
                'apps.main.context_processors.PhonesContext',
            ],
        },
    },
]


WSGI_APPLICATION = 'project.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'uk'
LANGUAGES = (
    ('uk', ('УКР')),
    ('en', ('ENG')),
)

TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = True
USE_TZ = True


LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# LANGUAGES = [{ language.code : language.name } for language in Languages.objects.all()]





STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    STATICFILE_DIR,
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


COMPRESS_ROOT = os.path.join(BASE_DIR, 'static/')

LOGIN_URL = "/login"


# E-mail
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = GMAIL_ADRESS
EMAIL_HOST_PASSWORD = GMAIL_PASSWORD
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# CART
CART_SESSION_ID = 'cart'
# WISHLIST
WISHLIST_SESSION_ID = 'wishlist'
# WATCHLIST
WATCHLIST_SESSION_ID = 'watchlist'

# Message
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# User
AUTH_USER_MODEL = 'user.CustomUser'
ACCOUNT_AUTHENTICATION_METHOD = "email"
# LOGOUT_REDIRECT_URL = '/'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'tmp/django_cache',
        'TIMEOUT': 60 * 60 * 24 * 365,
        'OPTIONS': {
            'MAX_ENTRIES': 10000
        }
    }
}


ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'localhost:9200'
    },
}



def create_filename(filename):
    import uuid
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4().hex, ext)
    return os.path.join('custom', filename)



# sentry_sdk.init(
#     dsn="https://6bb432ceb5bb4d749ddb1da802c35666@o362395.ingest.sentry.io/6593804",
#     integrations=[
#         DjangoIntegration(),
#     ],

#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0,

#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )

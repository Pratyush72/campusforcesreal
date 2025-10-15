from pathlib import Path
import razorpay
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'replace-this-with-a-secret-key'

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'careers',
    'realtime_chat',
    'channels',
    'admin_panel',

]


AUTH_USER_MODEL = 'accounts.CustomUser'
 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'campusforce.urls'

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

# ----------------------------

WSGI_APPLICATION = 'campusforce.wsgi.application'
ASGI_APPLICATION = 'campusforce.asgi.application'


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer", 
    }
}


# ----------------------------


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'campusforce_db',
#         'USER': 'campus_user',
#         'PASSWORD': 'Campus@2002',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'campusforce_db',
        'USER': 'campus_user',
        'PASSWORD': 'Campus@2002',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}



MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# RAZORPAY_KEY_ID = "rzp_test_tV8hhS0olbbfGd"
# RAZORPAY_KEY_SECRET = "bLZMe2pOY0hqOysqLAZriZoX"


RAZORPAY_KEY_ID = "rzp_live_RSb63M2buy7TOc"
RAZORPAY_SECRET_KEY = "J3x6K0novYS9ahUSWz6ng6BH"

# RAZORPAY_KEY_ID = "rzp_test_RSffuRbTZLQfzk"
# RAZORPAY_SECRET_KEY = "arYq72rZ7bolNIGLE68rtCaO"



AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/' 

INSTALLED_APPS += [
    'accounts',
]

AUTH_USER_MODEL = 'accounts.CustomUser'


AUTH_USER_MODEL = 'accounts.CustomUser'

# Email ke liye SMTP setup (OTP & Reset Password)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'noreplycampusforces@gmail.com'
EMAIL_HOST_PASSWORD = 'pkwm yfbo ppgq nfsg'
EMAIL_USE_TLS = True


AUTH_USER_MODEL = 'accounts.CustomUser'

# INSTALLED_APPS is already defined above and extended with 'accounts', so this redefinition is removed to avoid syntax errors.


AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'
USE_TZ = True
USE_I18N = True


import os

# Base directory already defined
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Add this line

# Optional: Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / "core/static"]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# TEMPLATE DIR setup
import os
TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, 'templates')]

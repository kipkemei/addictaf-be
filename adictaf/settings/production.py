from .base import *

# ALLOWED_HOSTS =config('ALLOWED_HOSTS', cast=Csv())

ALLOWED_HOSTS = ['*']
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

# CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST', cast=Csv())
CORS_ORIGIN_ALLOW_ALL = True

# TODO: Replace the below lines with valid ones
# STATIC_URL='/static/'
# STATIC_ROOT=os.path.join(LIVE_DIR, 'static')
#
# MEDIA_URL='/media/'
# MEDIA_ROOT=os.path.join(LIVE_DIR, 'media')
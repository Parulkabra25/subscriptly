from .base import *
DEBUG=True

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD':env("DATABASE_PASSWORD"),
        'HOST':env('DATABASE_HOST',default='localhost'),
        'PORT':env('DATABASE_PORT',default='5432'),
    }
}

# JWT Authentication (SimpleJWT)

REST_FRAMEWORK={
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
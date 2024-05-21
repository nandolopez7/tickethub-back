from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

DEF_DATABASE_URL=f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{env('POSTGRES_HOST')}:{env('POSTGRES_PORT')}/{env('POSTGRES_DB')}"

# DATABASES
DATABASES = {
    'default': env.db('DATABASE_URL', default=DEF_DATABASE_URL),
}

AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID', default="")
AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY', default="")
AWS_DEFAULT_REGION = env('AWS_DEFAULT_REGION')
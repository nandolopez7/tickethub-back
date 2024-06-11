from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


DEF_DATABASE_URL=f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{env('POSTGRES_HOST')}:{env('POSTGRES_PORT')}/{env('POSTGRES_DB')}"

# DATABASES
DATABASES = {
    'default': env.db('DATABASE_URL', default=DEF_DATABASE_URL),
}

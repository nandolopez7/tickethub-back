from .base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'tickethubapi.onrender.com',
    'tickethub-back.onrender.com',
]

CORS_ALLOWED_ORIGINS = [ 
    'http://localhost:3000',
    'https://tickethub-front.vercel.app'
]


# DATABASES
DATABASES = {
    'default': dj_database_url.config(default=env('DATABASE_URL'),  conn_max_age=600),
}

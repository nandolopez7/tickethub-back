from .base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'tickethubapi.onrender.com',
    'tickethub-back.onrender.com',
]

CORS_ALLOWED_ORIGINS = [ 
    'https://tickethub-front.vercel.app/'
]

# This production code might break development mode, so we check whether we're in DEBUG mode
STATIC_ROOT = os.path.join(ROOT_DIR, 'staticfiles')
# Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
# and renames the files with unique names for each version to support long-term caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# DATABASES
DATABASES = {
    'default': dj_database_url.config(default=env('DATABASE_URL'),  conn_max_age=600),
}

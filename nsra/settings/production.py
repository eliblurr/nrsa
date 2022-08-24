import os, random, string, dj_database_url, django_cache_url
from .base import *

DEBUG = os.getenv('DEBUG', 'off').lower()=='on'

# DJANGO_SECRET_KEY *should* be specified in the environment. If it's not, generate an ephemeral key.
SECRET_KEY = os.getenv('SECRET_KEY', None)
if bool(SECRET_KEY)==False:
    print("WARNING: SECRET_KEY not found in os.environ. Generating ephemeral SECRET_KEY.")
    SECRET_KEY = ''.join([random.SystemRandom().choice(string.printable) for i in range(50)])

# Make sure Django can detect a secure connection properly on Heroku:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Redirect all requests to HTTPS
SECURE_SSL_REDIRECT = os.getenv('DJANGO_SECURE_SSL_REDIRECT', 'off').lower()=='on'

ADMINS = [
    admin.split(',') for admin in os.getenv('ADMINS', 'admin,admin@admin.com;admin2,admin2@mail.com').split(';') if admin
]

# Accept all hostnames, since we don't know in advance which hostname will be used for any given Heroku instance.
# IMPORTANT: Set this to a real hostname when using this in production!
# See https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(';')

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.mailtrap.io')
EMAIL_PORT = os.getenv('EMAIL_PORT', 2525) 
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', True) in ['true', 'True', True, 0]
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', False) in ['true', 'True', True, 0]
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '829e507086a9d9') 
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'e6e1d4fe2a31d3') 
EMAIL_SSL_CERTFILE = os.getenv('EMAIL_SSL_CERTFILE', None) 
EMAIL_SSL_KEYFILE = os.getenv('EMAIL_SSL_KEYFILE', None) 
EMAIL_TIMEOUT = os.getenv('EMAIL_TIMEOUT', None) 
EMAIL_USE_LOCALTIME = os.getenv('EMAIL_USE_LOCALTIME', False) in ['true', 'True', True, 0]
EMAIL_SUBJECT_PREFIX = os.getenv('EMAIL_SUBJECT_PREFIX', '')

# BASE_URL required for notification emails
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# configure CACHES from CACHE_URL environment variable (defaults to locmem if no CACHE_URL is set)
if bool(os.getenv('CACHE_URL', None)): 
    CACHES = {'default': django_cache_url.config()}

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False 

# AWS creds may be used for S3 and/or Elasticsearch
AWS_REGION = os.getenv('AWS_REGION', '')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')

# Configure MEDIA_BUCKET_SERVICE, if present in os.environ
MBS = os.getenv('MEDIA_BUCKET_SERVICE', None).lower()

if MBS == 'aws':
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_AUTO_CREATE_BUCKET = True
    if 'storages' not in INSTALLED_APPS:
        INSTALLED_APPS.append('storages')
    MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

elif MBS == 'gs':
    GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME')
    GS_PROJECT_ID = os.getenv('GS_PROJECT_ID')
    GS_DEFAULT_ACL = 'publicRead'
    GS_AUTO_CREATE_BUCKET = True
    if 'storages' not in INSTALLED_APPS:
        INSTALLED_APPS.append('storages')
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# Configure Elasticsearch, if present in os.environ
# see https://docs.wagtail.org/en/stable/topics/search/backends.html
ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL', None)

if ELASTICSEARCH_URL:
    from elasticsearch import RequestsHttpConnection
    WAGTAILSEARCH_BACKENDS = {
        'default': {
            'BACKEND': 'wagtail.search.backends.elasticsearch5',
            'INDEX': 'nsra',
            'TIMEOUT': 5,
            'HOSTS': [{
                'host': ELASTICSEARCH_URL,
                'port': int(os.getenv('ELASTICSEARCH_PORT', '9200')),
                'use_ssl': os.getenv('ELASTICSEARCH_USE_SSL', 'off') == 'on',
                'verify_certs': os.getenv('ELASTICSEARCH_VERIFY_CERTS', 'off') == 'on',
            }],
            'OPTIONS': {
                'connection_class': RequestsHttpConnection,
            },
        }
    }

    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        from aws_requests_auth.aws_auth import AWSRequestsAuth # see https://github.com/davidmuller/aws-requests-auth
        WAGTAILSEARCH_BACKENDS['default']['HOSTS'][0]['http_auth'] = AWSRequestsAuth(
            aws_access_key=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_token=os.getenv('AWS_SESSION_TOKEN', ''),
            aws_host=ELASTICSEARCH_URL,
            aws_region=AWS_REGION,
            aws_service='es',
        )
       
    elif AWS_REGION:
        # No API keys in the environ, so attempt to discover them with Boto instead, per:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#configuring-credentials
        # This may be useful if your credentials are obtained via EC2 instance meta data.
        from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
        WAGTAILSEARCH_BACKENDS['default']['HOSTS'][0]['http_auth'] = BotoAWSRequestsAuth(
            aws_host=ELASTICSEARCH_URL,
            aws_region=AWS_REGION,
            aws_service='es',
        )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'mail': {
            'include_html': True,
            'class': 'django.utils.log.AdminEmailHandler',
            'level':  os.getenv('MAIL_LOG_LEVEL', 'CRITICAL'),
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': f'{BASE_DIR}/logs/debug.log',
            'level': os.getenv('FILE_LOG_LEVEL', 'ERROR'),
        },
        'info': {
            'class': 'logging.FileHandler',
            'filename': f'{BASE_DIR}/logs/info.log',
            'level': 'INFO',
        },
    },
    
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    
    'loggers': {
        '':{
            'handlers': ['file', 'mail'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['info'],
            'propagate': False,
            'level': 'INFO',
        },
    },
}
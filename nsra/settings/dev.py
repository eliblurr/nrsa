from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8k(9h10a)!)tdux8px7yesitkrez1q4=to*1ahp&p^b7#aljag'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_PORT = 2525
EMAIL_HOST_USER = os.getenv('EMAIL_USER', '829e507086a9d9')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD', 'e6e1d4fe2a31d3')
EMAIL_USE_TLS = os.getenv('USE_TLS', False)
EMAIL_USE_SSL = os.getenv('USE_SSL', False)

# BASE_URL required for notification emails
BASE_URL = 'http://localhost:8000'

# try:
#     from .local import *
# except ImportError:
#     pass

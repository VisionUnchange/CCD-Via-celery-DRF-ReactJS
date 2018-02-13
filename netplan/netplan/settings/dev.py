from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^6s-1p=xvt-6ourro=d*()m!8)&2kc0e9zl6ggea)-7*=4z$t^'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



try:
    from .local import *
except ImportError:
    pass

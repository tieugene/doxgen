"""
Sample for production doxgen
"""
DEBUG = False
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = '...'
ALLOWED_HOSTS = ['www.example.com']
STATIC_URL = '/static_doxgen/'
ADMINS = [('Admin', 'info@example.com')]
SERVER_EMAIL = [('DoxGen', 'robot@example.com')]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 'NAME': '/var/lib/doxgen/db.sqlite3'
    }
}
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': 'unix:/tmp/memcached.sock',
#     }
# }
LOGGERS = {     # simple 'LOGGING.uppend(...) not works
    'django': {
        'handlers': ['syslog'],
        'level': 'INFO',
        'disabled': False,
        'propagate': True
    }
}

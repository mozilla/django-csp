CSP_REPORT_ONLY = False

CSP_INCLUDE_NONCE_IN = ['default-src']

DATABASES = {
    'default': {
        'NAME': 'test.db',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'csp',
)

SECRET_KEY = 'csp-test-key'

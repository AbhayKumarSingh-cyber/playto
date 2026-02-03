DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Or sqlite3 for local
        'NAME': 'playto',
        'USER': 'playto_user',
        'PASSWORD': 'playto_pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
INSTALLED_APPS = ['rest_framework', 'community']
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'mailviews',
            'mailviews.tests',
        ),
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        ROOT_URLCONF='mailviews.tests.urls',
        STATIC_URL='/static/',
        LOGGING={
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                },
            },
            'loggers': {
                '': {
                    'handler': ['console'],
                    'level': 'DEBUG',
                },
            },
        },
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
            },
        ]
    )

    if hasattr(django, 'setup'):
        django.setup()


from mailviews.tests.tests import *  # NOQA

if __name__ == '__main__':
    from mailviews.tests.__main__ import __main__

    __main__()

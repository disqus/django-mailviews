from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=(
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
    )


from mailviews.tests.tests import *  # NOQA


def run():
    import sys
    from django.test.utils import get_runner

    runner = get_runner(settings)()
    failures = runner.run_tests(('mailviews',))
    sys.exit(failures)

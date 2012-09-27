from django.conf import settings

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=(
            'mailview',
        ),
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
    )


from mailview.tests.tests import *  # NOQA


def run():
    import sys
    from django.test.utils import get_runner

    runner = get_runner(settings)()
    failures = runner.run_tests(('mailview',))
    sys.exit(failures)

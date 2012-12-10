from django.conf import settings


def should_use_staticfiles():
    return 'django.contrib.staticfiles' in settings.INSTALLED_APPS

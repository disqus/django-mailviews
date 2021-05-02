from __future__ import absolute_import

from django import template

from mailviews.helpers import should_use_staticfiles
from mailviews.previews import URL_NAMESPACE


register = template.Library()


def mailviews_static(path):
    if should_use_staticfiles():
        from django.contrib.staticfiles.templatetags import staticfiles
        return staticfiles.static(path)
    else:
        from django.urls import reverse
        return reverse('%s:static' % URL_NAMESPACE, kwargs={
            'path': path,
        })


register.simple_tag(mailviews_static)

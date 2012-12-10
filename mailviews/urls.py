import os

from django.conf.urls.defaults import patterns, url

from mailviews.helpers import should_use_staticfiles


urlpatterns = patterns('')


if not should_use_staticfiles():
    urlpatterns += patterns('',
        url(regex=r'^static/(?P<path>.*)$',
            view='django.views.static.serve',
            kwargs={
                'document_root': os.path.join(os.path.dirname(__file__), 'static'),
            },
            name='mailviews-static'),
    )

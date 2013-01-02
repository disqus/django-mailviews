import os

from django.conf.urls.defaults import patterns, url

from mailviews.helpers import should_use_staticfiles
from mailviews.views import preview_detail, preview_list


urlpatterns = patterns('',
    url(regex=r'^$',
        view=preview_list,
        name='mailviews-preview-list'),
    url(regex=r'^(?P<module>.+)/(?P<identifier>.+)/$',
        view=preview_detail,
        name='mailviews-preview-detail'),
)


if not should_use_staticfiles():
    urlpatterns += patterns('',
        url(regex=r'^static/(?P<path>.*)$',
            view='django.views.static.serve',
            kwargs={
                'document_root': os.path.join(os.path.dirname(__file__), 'static'),
            },
            name='mailviews-static'),
    )

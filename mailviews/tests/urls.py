from django.conf.urls.defaults import include, patterns, url

from mailviews.tests.views import preview


urlpatterns = patterns('',
    url(regex=r'^$', view=preview),
    url(regex=r'^mailviews/', view=include('mailviews.urls')),
)

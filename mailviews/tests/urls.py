from django.conf.urls.defaults import include, patterns, url


urlpatterns = patterns('',
    url(regex=r'', view=include('mailviews.urls')),
)

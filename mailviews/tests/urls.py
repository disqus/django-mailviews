from django.conf.urls.defaults import include, patterns, url

from mailviews.previews import autodiscover, site


autodiscover()

urlpatterns = patterns('',
    url(regex=r'', view=site.urls),
)

from mailviews.utils import is_django_version_greater

if is_django_version_greater('1.9'):
    from django.conf.urls import include, url
else:
    from django.conf.urls import patterns, include, url


from mailviews.previews import autodiscover, site


autodiscover()

if is_django_version_greater('1.9'):
	urlpatterns = [
		url(regex=r'', view=site.urls)
	]
else:
	urlpatterns = patterns('',
	    url(regex=r'', view=site.urls),
	)

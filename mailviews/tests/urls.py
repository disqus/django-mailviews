from mailviews.utils import is_django_version_greater_than_1_9

if is_django_version_greater_than_1_9():
    from django.conf.urls import include, url
else:
    try:
        from django.conf.urls import patterns, include, url
    except ImportError:
        # Django <1.4 compat
        from django.conf.urls.defaults import patterns, include, url


from mailviews.previews import autodiscover, site


autodiscover()

if is_django_version_greater_than_1_9():
	urlpatterns = [
		url(regex=r'', view=site.urls)
	]
else:
	urlpatterns = patterns('',
	    url(regex=r'', view=site.urls),
	)

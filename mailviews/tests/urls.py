from django.conf.urls import include, url


from mailviews.previews import autodiscover, site


autodiscover()

urlpatterns = [
    url(regex=r'', view=site.urls)
]

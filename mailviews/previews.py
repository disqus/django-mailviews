import logging
import os
from base64 import b64encode
from collections import namedtuple

from django.conf.urls.defaults import include, patterns, url
from django.core.urlresolvers import reverse
from django.utils.datastructures import SortedDict
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from django.views.generic.simple import direct_to_template

from mailviews.helpers import should_use_staticfiles
from mailviews.utils import split_docstring, unimplemented


logger = logging.getLogger(__name__)


URL_NAMESPACE = 'mailviews'

ModulePreviews = namedtuple('ModulePreviews', ('module', 'previews'))


class PreviewSite(object):
    def __init__(self):
        self.__previews = {}

    def __iter__(self):
        for module in sorted(self.__previews.keys()):
            previews = ModulePreviews(module, sorted(self.__previews[module].values(), key=str))
            yield previews

    def register(self, cls):
        """
        Adds a preview to the index.
        """
        preview = cls(site=self)
        logger.debug('Registering %r with %r', preview, self)
        index = self.__previews.setdefault(preview.module, {})
        index[cls.__name__] = preview

    @property
    def urls(self):
        urlpatterns = patterns('',
            url(regex=r'^$',
                view=self.list_view,
                name='list'),
            url(regex=r'^(?P<module>.+)/(?P<preview>.+)/$',
                view=self.detail_view,
                name='detail'),
        )

        if not should_use_staticfiles():
            urlpatterns += patterns('',
                url(regex=r'^static/(?P<path>.*)$',
                    view='django.views.static.serve',
                    kwargs={
                        'document_root': os.path.join(os.path.dirname(__file__), 'static'),
                    },
                    name='static'),
                )

        return include(urlpatterns, namespace=URL_NAMESPACE)

    def list_view(self, request):
        return direct_to_template(request, 'mailviews/previews/list.html', {
            'site': self,
        })

    def detail_view(self, request, module, preview):
        return self.__previews[module][preview].detail_view(request)


class Preview(object):
    message_view = property(unimplemented)  # must be implemented by subclasses
    headers = ('Subject', 'From', 'To')
    verbose_name = None

    def __init__(self, site):
        self.site = site

    def __unicode__(self):
        return self.verbose_name or self.message_view.__name__

    @property
    def module(self):
        return '%s' % self.message_view.__module__

    @property
    def description(self):
        return getattr(split_docstring(self.message_view), 'summary', None)

    @property
    def url(self):
        return reverse('%s:detail' % URL_NAMESPACE, kwargs={
            'module': self.module,
            'preview': type(self).__name__,
        })

    def get_message_view(self, request):
        return self.message_view()

    def detail_view(self, request):
        """
        Renders the message view to a response.
        """
        message_view = self.get_message_view(request)

        message = message_view.render_to_message()
        raw = message.message()
        headers = SortedDict((header, raw[header]) for header in self.headers)

        context = {
            'preview': self,
            'message': message,
            'subject': message.subject,
            'body': message.body,
            'headers': headers,
            'raw': raw.as_string(),
        }

        alternatives = getattr(message, 'alternatives', [])
        try:
            html = next(alternative[0] for alternative in alternatives
                if alternative[1] == 'text/html')
            context.update({
                'html': html,
                'escaped_html': b64encode(html),
            })
        except StopIteration:
            pass

        return direct_to_template(request, 'mailviews/previews/detail.html', context)


def autodiscover():
    from django.conf import settings
    for application in settings.INSTALLED_APPS:
        module = import_module(application)
        try:
            import_module('%s.emails.previews' % application)
        except ImportError:
            if module_has_submodule(module, 'emails.previews'):
                raise


site = PreviewSite()

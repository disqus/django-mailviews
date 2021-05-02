import logging
import os
from base64 import b64encode
from collections import namedtuple
from email.header import decode_header

import django
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

from django.utils.module_loading import module_has_submodule

from mailviews.helpers import should_use_staticfiles
from mailviews.utils import split_docstring, unimplemented

from django.conf.urls import include, url


logger = logging.getLogger(__name__)


URL_NAMESPACE = 'mailviews'

ModulePreviews = namedtuple('ModulePreviews', ('module', 'previews'))


def maybe_decode_header(header):
    """
    Decodes an encoded 7-bit ASCII header value into it's actual value.
    """
    value, encoding = decode_header(header)[0]
    if encoding:
        return value.decode(encoding)
    else:
        return value


class PreviewSite(object):
    def __init__(self):
        self.__previews = {}

    def __iter__(self):
        """
        Returns an iterator of :class:`ModulePreviews` tuples, sorted by module nae.
        """
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

        urlpatterns = [
            url(regex=r'^$',
                view=self.list_view,
                name='list'),
            url(regex=r'^(?P<module>.+)/(?P<preview>.+)/$',
                view=self.detail_view,
                name='detail'),
        ]

        if not should_use_staticfiles():
            url_staticsfiles = [
                url(regex=r'^static/(?P<path>.*)$',
                    view=django.views.static.serve,
                    kwargs={
                        'document_root': os.path.join(os.path.dirname(__file__), 'static'),
                    },
                    name='static')
            ]

            urlpatterns += url_staticsfiles

        return include(urlpatterns, namespace=URL_NAMESPACE)

    def list_view(self, request):
        """
        Returns a list view response containing all of the registered previews.
        """
        return render(request, 'mailviews/previews/list.html', {
            'site': self,
        })

    def detail_view(self, request, module, preview):
        """
        Looks up a preview in the index, returning a detail view response.
        """
        try:
            preview = self.__previews[module][preview]
        except KeyError:
            raise Http404  # The provided module/preview does not exist in the index.
        return preview.detail_view(request)


class Preview(object):
    #: The message view class that will be instantiated to render the preview
    #: message. This must be defined by subclasses.
    message_view = property(unimplemented)

    #: The subset of headers to show in the preview panel.
    headers = ('Subject', 'From', 'To')

    #: The title of this email message to use in the previewer. If not provided,
    #: this will default to the name of the message view class.
    verbose_name = None

    #: A form class that will be used to customize the instantiation behavior
    # of the message view class.
    form_class = None

    #: The template that will be rendered for this preview.
    template_name = 'mailviews/previews/detail.html'

    def __init__(self, site):
        self.site = site

    def __unicode__(self):
        return self.verbose_name or self.message_view.__name__

    @property
    def module(self):
        return '%s' % self.message_view.__module__

    @property
    def description(self):
        """
        A longer description of this preview that is used in the preview index.

        If not provided, this defaults to the first paragraph of the underlying
        message view class' docstring.
        """
        return getattr(split_docstring(self.message_view), 'summary', None)

    @property
    def url(self):
        """
        The URL to access this preview.
        """
        return reverse('%s:detail' % URL_NAMESPACE, kwargs={
            'module': self.module,
            'preview': type(self).__name__,
        })

    def get_message_view(self, request, **kwargs):
        return self.message_view(**kwargs)

    def detail_view(self, request):
        """
        Renders the message view to a response.
        """
        context = {
            'preview': self,
        }

        kwargs = {}
        if self.form_class:
            if request.GET:
                form = self.form_class(data=request.GET)
            else:
                form = self.form_class()

            context['form'] = form
            if not form.is_bound or not form.is_valid():
                return render(request, 'mailviews/previews/detail.html', context)

            kwargs.update(form.get_message_view_kwargs())

        message_view = self.get_message_view(request, **kwargs)

        message = message_view.render_to_message()
        raw = message.message()
        headers = OrderedDict((header, maybe_decode_header(raw[header])) for header in self.headers)

        context.update({
            'message': message,
            'subject': message.subject,
            'body': message.body,
            'headers': headers,
            'raw': raw.as_string(),
        })

        alternatives = getattr(message, 'alternatives', [])
        try:
            html = next(alternative[0] for alternative in alternatives
                if alternative[1] == 'text/html')
            context.update({
                'html': html,
                'escaped_html': b64encode(html.encode('utf-8')),
            })
        except StopIteration:
            pass

        return render(request, self.template_name, context)


def autodiscover():
    """
    Imports all available previews classes.
    """
    from django.conf import settings
    for application in settings.INSTALLED_APPS:
        module = import_module(application)

        if module_has_submodule(module, 'emails'):
            emails = import_module('%s.emails' % application)
            try:
                import_module('%s.emails.previews' % application)
            except ImportError:
                # Only raise the exception if this module contains previews and
                # there was a problem importing them. (An emails module that
                # does not contain previews is not an error.)
                if module_has_submodule(emails, 'previews'):
                    raise


#: The default preview site.
site = PreviewSite()

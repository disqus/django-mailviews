import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

from mailviews.utils import unimplemented


logger = logging.getLogger(__name__)

registry = {}


class Preview(object):
    message_view = property(unimplemented)  # must be implemented by subclasses
    description = None
    verbose_name = None

    def __str__(self):
        return self.verbose_name or self.message_view.__name__

    @property
    def module(self):
        return '%s' % self.message_view.__module__

    @property
    def identifier(self):
        return self.message_view.__name__

    @property
    def url(self):
        return reverse('mailviews-preview-detail', kwargs={
            'module': self.module,
            'identifier': self.identifier
        })

    def get_message_view(self, request):
        return self.message_view()


def register(preview):
    logger.debug('Registering %s...', preview)
    preview = preview()
    registry.setdefault(preview.module, {})[preview.identifier] = preview


def autodiscover():
    for application in settings.INSTALLED_APPS:
        module = import_module(application)
        try:
            import_module('%s.emails' % application)
        except ImportError:
            if module_has_submodule(module, 'emails'):
                raise

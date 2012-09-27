from django.core.exceptions import ImproperlyConfigured
from django.core.mail.message import EmailMessage, EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template, select_template

from mailview.utils import unescape


class EmailMessageView(object):
    """
    Base class for rendering and sending class-based email messages.
    """
    message_class = EmailMessage

    def render_subject(self, context):
        raise NotImplementedError  # Must be implemented by subclasses.

    def render_body(self, context):
        raise NotImplementedError  # Must be implemented by subclasses.

    def get_context_data(self, **kwargs):
        return Context(kwargs)

    def render_to_message(self, context, **kwargs):
        return self.message_class(
            subject=self.render_subject(context),
            body=self.render_body(context),
            **kwargs)

    def send(self, extra_context=None, **kwargs):
        """
        Renders and sends an email message.

        All keyword arguments other than ``context`` are passed through as
        keyword arguments when constructing a new :attr:`message_class`
        instance for this message.

        :param extra_context: Any additional context data that will be used
            when rendering this message.
        :type context: :class:`dict`
        """
        if extra_context is None:
            extra_context = {}

        message = self.render_to_message(self.get_context_data(**extra_context),
            **kwargs)
        return message.send()


class TemplatedEmailMessageView(EmailMessageView):
    """
    An email message view that uses Django templates for rendering the message
    subject and plain text body.
    """
    subject_template_name = None
    body_template_name = None

    def _get_template(self, value):
        if isinstance(value, (list, tuple)):
            return select_template(value)
        else:
            return get_template(value)

    def _get_subject_template(self):
        if getattr(self, '_subject_template', None) is not None:
            return self._subject_template

        if self.subject_template_name is None:
            raise ImproperlyConfigured('A subject template name must be provided.')

        return self._get_template(self.subject_template_name)

    def _set_subject_template(self, template):
        self._subject_template = template

    subject_template = property(_get_subject_template, _set_subject_template)

    def _get_body_template(self):
        if getattr(self, '_body_template', None) is not None:
            return self._body_template

        if self.body_template_name is None:
            raise ImproperlyConfigured('A body template filename must be provided.')

        return self._get_template(self.body_template_name)

    def _set_body_template(self, template):
        self._body_template = template

    body_template = property(_get_body_template, _set_body_template)

    def render_subject(self, context):
        rendered = self.subject_template.render(unescape(context))
        return rendered.strip()

    def render_body(self, context):
        return self.body_template.render(unescape(context))


class TemplatedHTMLEmailMessageView(TemplatedEmailMessageView):
    """
    An email message view that uses Django templates for rendering the message
    subject, plain text and HTML body.
    """
    message_class = EmailMultiAlternatives

    html_body_template_name = None

    def _get_html_body_template(self):
        if getattr(self, '_html_body_template', None) is not None:
            return self._html_body_template

        if self.html_body_template_name is None:
            raise ImproperlyConfigured('A HTML template must be provided.')

        return self._get_template(self.html_body_template_name)

    def _set_html_body_template(self, template):
        self._html_body_template = template

    html_body_template = property(_get_html_body_template, _set_html_body_template)

    def render_html_body(self, context):
        return self.html_body_template.render(context)

    def render_to_message(self, context, *args, **kwargs):
        message = super(TemplatedHTMLEmailMessageView, self).render_to_message(context, *args, **kwargs)
        message.attach_alternative(content=self.render_html_body(context), mimetype='text/html')
        return message

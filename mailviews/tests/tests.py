import functools
import os

from django.core.exceptions import ImproperlyConfigured
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.template import Template, TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse

from mailviews.messages import (TemplatedEmailMessageView,
                                TemplatedHTMLEmailMessageView)
from mailviews.previews import URL_NAMESPACE
from mailviews.tests.emails.views import (BasicEmailMessageView,
                                          BasicHTMLEmailMessageView)
from mailviews.tests.emails.previews import (BasicPreview,
                                             BasicHTMLPreview,
                                             CustomizablePreview)
from mailviews.utils import split_docstring


try:
    from django.test.utils import override_settings
except ImportError:
    from mailviews.tests.utils import override_settings  # noqa


using_test_templates = override_settings(
    TEMPLATE_DIRS=(
        os.path.join(os.path.dirname(__file__), 'templates'),
    ),
    TEMPLATE_LOADERS=(
        'django.template.loaders.filesystem.Loader',
    )
)


class EmailMessageViewTestCase(TestCase):
    def run(self, *args, **kwargs):
        with using_test_templates:
            return super(EmailMessageViewTestCase, self).run(*args, **kwargs)

    def assertTemplateExists(self, name):
        try:
            get_template(name)
        except TemplateDoesNotExist:
            raise AssertionError('Template does not exist: %s' % name)

    def assertTemplateDoesNotExist(self, name):
        try:
            self.assertTemplateExists(name)
        except AssertionError:
            return
        raise AssertionError('Template exists: %s' % name)

    def assertOutboxLengthEquals(self, length):
        self.assertEqual(len(mail.outbox), length)


class TemplatedEmailMessageViewTestCase(EmailMessageViewTestCase):
    message_class = TemplatedEmailMessageView

    def setUp(self):
        self.message = self.message_class()

        self.template = 'Hello, world!'

        self.subject = 'subject'
        self.subject_template = Template('{{ subject }}')

        self.body = 'body'
        self.body_template = Template('{{ body }}')

        self.context_dict = {
            'subject': self.subject,
            'body': self.body,
        }

        self.context = self.context_dict

        self.render_subject = functools.partial(self.message.render_subject,
            context=self.context)
        self.render_body = functools.partial(self.message.render_body,
            context=self.context)

    def add_templates_to_message(self):
        """
        Adds templates to the fixture message, ensuring it can be rendered.
        """
        self.message.subject_template = self.subject_template
        self.message.body_template = self.body_template

    def test_subject_template_unconfigured(self):
        self.assertRaises(ImproperlyConfigured, self.render_subject)

    def test_subject_invalid_template_name(self):
        template = 'invalid.txt'
        self.assertTemplateDoesNotExist(template)

        self.message.subject_template_name = template
        self.assertRaises(TemplateDoesNotExist, self.render_subject)

    def test_subject_template_name(self):
        template = 'subject.txt'
        self.assertTemplateExists(template)

        self.message.subject_template_name = template
        self.assertEqual(self.render_subject(), self.subject)

    def test_subject_template(self):
        self.message.subject_template = self.subject_template
        self.assertEqual(self.render_subject(), self.subject)

    def test_body_template_unconfigured(self):
        self.assertRaises(ImproperlyConfigured, self.render_body)

    def test_body_invalid_template_name(self):
        template = 'invalid.txt'
        self.assertTemplateDoesNotExist(template)

        self.message.body_template_name = template
        self.assertRaises(TemplateDoesNotExist, self.render_body)

    def test_body_template_name(self):
        template = 'body.txt'
        self.assertTemplateExists(template)

        self.message.body_template_name = template
        self.assertEqual(self.render_body(), self.body + '\n')

    def test_body_template(self):
        self.message.body_template = self.body_template
        self.assertEqual(self.render_body(), self.body)

    def test_render_to_message(self):
        self.add_templates_to_message()
        message = self.message.render_to_message(self.context_dict)
        self.assertEqual(message.subject, self.subject)
        self.assertEqual(message.body, self.body)

    def test_send(self):
        self.add_templates_to_message()
        self.message.send(self.context_dict, to=('ted@disqus.com',))
        self.assertOutboxLengthEquals(1)

    def test_custom_headers(self):
        self.add_templates_to_message()
        address = 'ted@disqus.com'
        self.message.headers['Reply-To'] = address
        self.assertEqual(self.message.headers['Reply-To'], address)

        rendered = self.message.render_to_message()
        self.assertEqual(rendered.extra_headers['Reply-To'], address)

        rendered = self.message.render_to_message(headers={
            'References': 'foo',
        })
        self.assertEqual(rendered.extra_headers['Reply-To'], address)
        self.assertEqual(rendered.extra_headers['References'], 'foo')


class TemplatedHTMLEmailMessageViewTestCase(TemplatedEmailMessageViewTestCase):
    message_class = TemplatedHTMLEmailMessageView

    def setUp(self):
        super(TemplatedHTMLEmailMessageViewTestCase, self).setUp()

        self.html_body = 'html body'
        self.html_body_template = Template('{{ html }}')

        self.context_dict['html'] = self.html_body
        self.context['html'] = self.html_body

        self.render_html_body = functools.partial(
            self.message.render_html_body,
            context=self.context)

    def add_templates_to_message(self):
        """
        Adds templates to the fixture message, ensuring it can be rendered.
        """
        super(TemplatedHTMLEmailMessageViewTestCase, self)\
            .add_templates_to_message()
        self.message.html_body_template = self.html_body_template

    def test_html_body_template_unconfigured(self):
        self.assertRaises(ImproperlyConfigured, self.render_html_body)

    def test_html_body_invalid_template_name(self):
        template = 'invalid.txt'
        self.assertTemplateDoesNotExist(template)

        self.message.html_body_template_name = template
        self.assertRaises(TemplateDoesNotExist, self.render_html_body)

    def test_html_body_template_name(self):
        template = 'body.html'
        self.assertTemplateExists(template)

        self.message.html_body_template_name = template
        self.assertEqual(self.render_html_body(), self.html_body + '\n')

    def test_html_body_template(self):
        self.message.html_body_template = self.html_body_template
        self.assertEqual(self.render_html_body(), self.html_body)

    def test_render_to_message(self):
        self.add_templates_to_message()
        message = self.message.render_to_message(self.context_dict)
        self.assertEqual(message.subject, self.subject)
        self.assertEqual(message.body, self.body)
        self.assertEqual(message.alternatives, [(self.html_body, 'text/html')])

    def test_send(self):
        self.add_templates_to_message()
        self.message.send(self.context_dict, to=('ted@disqus.com',))
        self.assertOutboxLengthEquals(1)


class SplitDocstringTestCase(TestCase):
    def test_split_docstring(self):
        header, body = split_docstring(split_docstring)
        self.assertEqual(header, "Splits the docstring of the given value into it's summary and body.")

    def test_split_docstring_no_body(self):
        def fn():
            """Does a thing."""

        header, body = split_docstring(fn)
        self.assertEqual(header, "Does a thing.")


class PreviewSiteTestCase(TestCase):

    def setUp(self):
        super(PreviewSiteTestCase, self).setUp()
        self.client = Client()

    def test_basic_preview(self):
        url = reverse('%s:detail' % URL_NAMESPACE, kwargs={
            'module': BasicEmailMessageView.__module__,
            'preview': BasicPreview.__name__
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '#body-plain')
        self.assertContains(response, '#raw')

    def test_basic_html_preview(self):
        url = reverse('%s:detail' % URL_NAMESPACE, kwargs={
            'module': BasicHTMLEmailMessageView.__module__,
            'preview': BasicHTMLPreview.__name__
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '#html')
        self.assertContains(response, '#body-plain')
        self.assertContains(response, '#raw')

    def test_customizable_preview(self):
        url = reverse('%s:detail' % URL_NAMESPACE, kwargs={
            'module': BasicEmailMessageView.__module__,
            'preview': CustomizablePreview.__name__
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertContains(response, '#body-plain')
        self.assertContains(response, '#raw')

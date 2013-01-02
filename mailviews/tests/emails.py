import random

from django.contrib.webdesign.lorem_ipsum import paragraphs, words
from django.template import Template

from mailviews.previews import Preview, register
from mailviews.messages import (TemplatedEmailMessageView,
    TemplatedHTMLEmailMessageView)


class TemplateContextMixin(object):
    subject_template = Template('{{ subject }}')
    body_template = Template('{{ content }}')

    def __init__(self, subject, content):
        self.subject = subject
        self.content = content

    def get_context_data(self, *args, **kwargs):
        data = super(TemplateContextMixin, self).get_context_data(*args, **kwargs)
        data.update({
            'subject': self.subject,
            'content': self.content,
        })
        return data


class BasicEmailMessageView(TemplateContextMixin, TemplatedEmailMessageView):
    pass


class BasicHTMLEmailMessageView(TemplateContextMixin, TemplatedHTMLEmailMessageView):
    html_body_template = Template('{{ content|linebreaks }}')


class BasicPreview(Preview):
    message_view = BasicEmailMessageView
    verbose_name = 'Basic Message'
    description = 'A basic text email message.'

    def get_message_view(self, request):
        subject = words(random.randint(5, 20), common=False)
        content = '\n'.join(paragraphs(random.randint(3, 6)))
        return self.message_view(subject, content)


class BasicHTMLPreview(BasicPreview):
    message_view = BasicHTMLEmailMessageView
    verbose_name = 'Basic HTML Message'
    description = 'A basic HTML email message.'


register(BasicPreview)
register(BasicHTMLPreview)

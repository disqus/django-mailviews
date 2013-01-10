from django.template import Template

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

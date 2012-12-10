import random

from django.contrib.webdesign.lorem_ipsum import paragraphs, words
from django.template import Template

from mailviews.messages import (TemplatedEmailMessageView,
    TemplatedHTMLEmailMessageView)
from mailviews.views import render_message_to_response


def preview(request):
    html = 'html' in request.GET

    if html:
        view_cls = TemplatedHTMLEmailMessageView
    else:
        view_cls = TemplatedEmailMessageView

    message_view = view_cls()
    message_view.subject_template = Template('{{ subject }}')
    message_view.body_template = Template('{{ content }}')
    if html:
        message_view.html_body_template = Template('{{ content|linebreaks }}')

    message = message_view.render_to_message(extra_context={
        'subject': words(random.randint(5, 20), common=False),
        'content': '\n'.join(paragraphs(random.randint(3, 6))),
    })
    return render_message_to_response(request, message)

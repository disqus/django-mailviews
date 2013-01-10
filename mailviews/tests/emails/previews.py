import random

from django.contrib.webdesign.lorem_ipsum import paragraphs, words

from mailviews.previews import Preview, site
from mailviews.tests.emails.views import (BasicEmailMessageView,
    BasicHTMLEmailMessageView)


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


site.register(BasicPreview)
site.register(BasicHTMLPreview)

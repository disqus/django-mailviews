import random

from django import forms
try:
    from django.utils.lorem_ipsum import words, paragraphs
except ImportError:
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


class CustomizationForm(forms.Form):
    subject = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

    def get_message_view_kwargs(self):
        return self.cleaned_data


class CustomizablePreview(Preview):
    message_view = BasicEmailMessageView
    verbose_name = 'Basic Message, with Form'
    description = 'A basic text email message, but customizable.'
    form_class = CustomizationForm


site.register(BasicPreview)
site.register(BasicHTMLPreview)
site.register(CustomizablePreview)

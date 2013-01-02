from base64 import b64encode
from django.views.generic.simple import direct_to_template
from django.utils.datastructures import SortedDict

from mailviews.previews import registry


def preview_list(request):
    context = {
        'registry': registry,
    }
    return direct_to_template(request, 'mailviews/previews/list.html', extra_context=context)


def preview_detail(request, module, identifier):
    preview = registry[module][identifier]

    message_view = preview.get_message_view(request)
    message = message_view.render_to_message()

    raw_message = message.message()

    headers = SortedDict(item for item in raw_message.items() if item[0] in ('Subject', 'From', 'To'))
    subject = headers.pop('Subject', None)
    if subject is not None:
        headers.insert(0, 'Subject', subject)

    context = {
        'preview': preview,
        'message_view': message_view,
        'message': message,
        'subject': message.subject,
        'body': message.body,
        'headers': headers,
        'raw': raw_message.as_string(),
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

    return direct_to_template(request, 'mailviews/previews/detail.html', extra_context=context)

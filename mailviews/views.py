from base64 import b64encode
from django.views.generic.simple import direct_to_template


def render_message_to_response(request, message):
    """
    A generic view that renders an email message preview to an HTTP response.

    :param request: An HTTP request.
    :type request: :class:`django.http.HttpRequest` instance
    :param message: An email message.
    :type message: :class:`django.core.mail.EmailMessage` instance
    :returns: An HTTP response.
    :rtype: :class:`django.http.HttpResponse`
    """
    raw_message = message.message()
    context = {
        'message': message,
        'subject': message.subject,
        'body': message.body,
        'headers': raw_message.items,
        'raw': raw_message.as_string(),
    }

    alternatives = getattr(message, 'alternatives', [])
    try:
        html = next(alternative[0] for alternative in alternatives
            if alternative[1] == 'text/html')
        context['html'] = b64encode(html)
    except StopIteration:
        pass

    return direct_to_template(request, 'mailviews/message.html',
        extra_context=context)

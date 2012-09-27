from django.template import Context


def unescape(context):
    """
    Accepts a context object, returning a new context object with autoescape off.

    Useful for rendering plain-text templates without having to wrap the entire
    template in an `{% autoescape off %}` tag.
    """
    return Context(context, autoescape=False)

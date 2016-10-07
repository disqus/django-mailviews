import textwrap
from collections import namedtuple

import django
from django.template import Context
from distutils.version import StrictVersion


Docstring = namedtuple('Docstring', ('summary', 'body'))


def split_docstring(value):
    """
    Splits the docstring of the given value into it's summary and body.

    :returns: a 2-tuple of the format ``(summary, body)``
    """
    docstring = textwrap.dedent(getattr(value, '__doc__', ''))
    if not docstring:
        return None

    pieces = docstring.strip().split('\n\n', 1)
    try:
        body = pieces[1]
    except IndexError:
        body = None

    return Docstring(pieces[0], body)


def unimplemented(*args, **kwargs):
    raise NotImplementedError


def unescape(context):
    """
    Accepts a context object, returning a new context with autoescape off.

    Useful for rendering plain-text templates without having to wrap the entire
    template in an `{% autoescape off %}` tag.
    """
    return Context(context, autoescape=False)

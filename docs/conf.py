import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from mailviews import __version__

import django
from django.conf import settings

if not settings.configured:
    settings.configure()


extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']

project = u'django-mailviews'
copyright = u'2012, DISQUS'
version = release = '.'.join(map(str, __version__))

html_static_path = ['_static']
htmlhelp_basename = 'django-mailviews'

intersphinx_mapping = {
    'python': ('http://docs.python.org/release/%s.%s' % sys.version_info[:2], None),
    'django': ('http://docs.djangoproject.com/en/%s.%s/' % django.VERSION[:2],
        'http://docs.djangoproject.com/en/%s.%s/_objects/' % django.VERSION[:2]),
}

autodoc_member_order = 'bysource'
autodoc_default_flags = ('members',)

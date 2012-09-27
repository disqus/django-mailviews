#!/usr/bin/env python
import os
import sys

from setuptools import find_packages, setup


def get_version():
    from mailview import __version__
    return '.'.join(map(str, __version__))

try:
    version = get_version()
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'mailview'))
    version = get_version()


install_requires = ['django']

setup(name='django-mailview',
    version=version,
    url='http://github.com/disqus/django-mailview/',
    author='ted kaemming',
    author_email='ted@disqus.com',
    description='Class-based mail views for Django',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    test_suite='mailview.tests.run',
    zip_safe=False,
)

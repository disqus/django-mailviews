#!/usr/bin/env python
import os
import sys

from setuptools import find_packages, setup


def get_version():
    from mailviews import __version__
    return '.'.join(map(str, __version__))

try:
    version = get_version()
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'mailviews'))
    version = get_version()


install_requires = ['django']

setup(name='django-mailviews',
    version=version,
    url='http://github.com/disqus/django-mailviews/',
    author='ted kaemming',
    author_email='ted@disqus.com',
    description='Class-based mail views for Django',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    test_suite='mailviews.tests.run',
    zip_safe=False,
)

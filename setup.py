#!/usr/bin/env python
from setuptools import find_packages, setup


install_requires = ['django']

setup(name='django-mailviews',
    version='0.5.3',
    url='http://github.com/disqus/django-mailviews/',
    author='ted kaemming',
    author_email='ted@disqus.com',
    description='Class-based mail views for Django',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    test_suite='mailviews.tests.run',
    zip_safe=False,
    license='Apache License 2.0',
)

#!/usr/bin/env python
from setuptools import find_packages, setup


setup(name='django-mailviews',
    version='0.6.5',
    url='http://github.com/disqus/django-mailviews/',
    author='ted kaemming',
    author_email='ted@disqus.com',
    description='Class-based mail views for Django',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=1.3',
    ],
    test_suite='mailviews.tests.__main__.__main__',
    zip_safe=False,
    license='Apache License 2.0',
)

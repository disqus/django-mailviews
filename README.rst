django-mailview
===============

Class-based email views for the Django framework, including a message previewer.

Testing and Development
-----------------------

Tested on Python 2.6 and 2.7, as well as Django 1.2, 1.3 and 1.4.

To run the test suite against your installed Django version, run
``python setup.py test``, or ``make test``. (If Django isn't already installed,
the latest stable version will be installed.)

All tests will automatically be run using the Django test runner when you run
the tests for your own projects if you use ``python manage.py test`` and
``mailview`` is within your ``settings.INSTALLED_APPS``.

To run tests against the entire build matrix, install
`tox <http://pypi.python.org/pypi/tox>`_ and run ``tox`` in the root of the
repository.

To view an example message preview, you can start a test server by running::

    $ python mailview/tests/manage.py runserver

and visiting http://127.0.0.1:8000/ for a plain text message preview, and
http://127.0.0.1:8000/?html for an HTML message preview.

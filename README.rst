django-mailviews
================

Class-based email views for the Django framework, including a message previewer.

.. image:: https://travis-ci.org/disqus/django-mailviews.png?branch=master
   :target: https://travis-ci.org/disqus/django-mailviews

Introduction
------------

Rendering and sending emails in Django can quickly become repetitive and
error-prone. By encapsulating message rendering within view classes, you can
easily compose messages in a structured and clear manner.

Basic Usage
-----------

.. code:: python

    from mailviews.messages import EmailMessageView

    # Subclass the `EmailMessageView`, adding the templates you want to render.
    class WelcomeMessageView(EmailMessageView):
        subject_template_name = 'emails/welcome/subject.txt'
        body_template_name = 'emails/welcome/body.txt'

    # Instantiate and send a message.
    message = WelcomeMessageView().send(extra_context={
        'user': user,
    }, to=(user.email,))

This isn't actually the best pattern for sending messages to a user -- read the
notes under "Best Practices" for a better approach.

Using the Preview Site
----------------------

Registering URLs and Enabling Discovery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Add ``mailviews`` to your project's ``INSTALLED_APPS`` setting.
* Add the following somewhere within your project's ``ROOT_URLCONF``:

.. code:: python

    from mailviews.previews import autodiscover, site

    autodiscover()

    urlpatterns = patterns('',
        url(regex=r'^emails/', view=site.urls),
    )

The preview index will now be available at the ``emails/`` URL.

Creating Preview Classes
~~~~~~~~~~~~~~~~~~~~~~~~

To create a simple preview, add a ``emails.previews`` submodule within one of your
``INSTALLED_APPS``, and create a new subclass of ``Preview``.

.. code:: python

    from mailviews.previews import Preview, site
    from example.emails.views import WelcomeMessageView

    # Define a new preview class.
    class BasicPreview(Preview):
        message_view = WelcomeMessageView

    # Register the preview class with the preview index.
    site.register(BasicPreview)

You can see more detailed examples within the `test suite <https://github.com/disqus/django-mailviews/blob/master/mailviews/tests/emails/previews.py>`_
or in the code documentation for ``mailviews.previews``.

Customizing Preview Behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use Django forms to customize the creation of message previews by
adding a ``form_class`` attribute to your ``Preview`` subclasses. The form must
provide a ``get_message_view_kwargs`` method that returns a the keyword arguments
to be used when constructing the message view instance.

Best Practices
--------------

* Try and avoid using the ``extra_context`` argument when sending emails.
  Instead, create an ``EmailMessageView`` subclass whose constructor accepts
  as arguments all of the objects that you require to generate the context and
  send the message. For example, the code shown in "Basic Usage" could written
  instead as the following:

.. code:: python

    from mailviews.messages import EmailMessageView

    class WelcomeMessageView(EmailMessageView):
        subject_template_name = 'emails/welcome/subject.txt'
        body_template_name = 'emails/welcome/body.txt'

        def __init__(self, user, *args, **kwargs):
            super(WelcomeMessageView, self).__init__(*args, **kwargs)
            self.user = user

        def get_context_data(self, **kwargs):
            context = super(WelcomeMessageView, self).get_context_data(**kwargs)
            context['user'] = self.user
            return context

        def render_to_message(self, *args, **kwargs):
            assert 'to' not in kwargs  # this should only be sent to the user
            kwargs['to'] = (self.user.email,)
            return super(WelcomeMessageView, self).render_to_message(*args, **kwargs)

    # Instantiate and send a message.
    WelcomeMessageView(user).send()

In fact, you might find it helpful to encapsulate the above "message for a user"
pattern into a mixin or subclass that provides a standard abstraction for all
user-related emails. (This is left as an exercise for the reader.)

Testing and Development
-----------------------

Tested on Python 2.6 and 2.7, as well as Django 1.2, 1.3 and 1.4.

To run the test suite against your installed Django version, run
``python setup.py test``, or ``make test``. (If Django isn't already installed,
the latest stable version will be installed.)

All tests will automatically be run using the Django test runner when you run
the tests for your own projects if you use ``python manage.py test`` and
``mailviews`` is within your ``settings.INSTALLED_APPS``.

To run tests against the entire build matrix, run ``make test-matrix``.

To view an example preview site, you can start a test server by running
``make test-server`` and visiting http://127.0.0.1:8000/.

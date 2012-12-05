django-mailviews
================

Class-based email views for the Django framework, including a message previewer.

Introduction
------------

Rendering and sending emails in Django can quickly become repetative and
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
    message = WelcomeMessageView()
    message.send(extra_context={
        'user': user,
    }, to=(user.email,))

This isn't actually the best pattern for sending messages to a user -- read the
notes under "Best Practices" for a better approach.

Best Practices
--------------

* Keep all of your message view subclasses in an ``emails`` module in your
  application.
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

To view an example message preview, you can start a test server by running
``make test-server`` and visiting http://127.0.0.1:8000/ for a plain text
message preview, and http://127.0.0.1:8000/?html for an HTML message preview.

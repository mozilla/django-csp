.. _installation-chapter:

=====================
Installing django-csp
=====================

First, install django-csp via pip or from source::

    # pip
    $ pip install django_csp

::

    # source
    $ git clone https://github.com/mozilla/django-csp.git
    $ cd django-csp
    $ python setup.py install

Now edit your project's ``settings`` module. If you are not using the
built in report processor, all you need to do is::

    MIDDLEWARE_CLASSES = (
        # ...
        'csp.middleware.CSPMiddleware',
        # ...
    )

If you are using the built-in processor, you'll also need to do this::


    INSTALLED_APPS = (
        # ...
        'csp',
        # ...
    )

    CSP_REPORT_URL = '/csp/reports'

And finally include the urlconf::

    urlpatterns = patterns('',
        # ...
        url(r'^csp', include('csp.urls')),
        # ...
    )

If you're using the default report processor, you'll need to run
``syncdb`` or ``migrate``, if you're using South_, or else create the
database tables another way.

That should do it! Go on to `configuring CSP <configuration-chapter>`_.

.. _South: http://south.aeracode.org/

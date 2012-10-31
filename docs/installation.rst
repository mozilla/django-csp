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

Now edit your project's ``settings`` module [#]_::

    MIDDLEWARE_CLASSES = (
        # ...
        'csp.middleware.CSPMiddleware',
        # ...
    )

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

That should do it! Go on to `configuring CSP <configuration-chapter>`_.

.. [#] Strictly speaking, ``csp`` only needs to be in your installed apps
   if you plan to use the built-in report feature.

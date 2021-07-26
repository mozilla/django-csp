.. _installation-chapter:

=====================
Installing django-csp
=====================

First, install django-csp via pip or from source::

    # pip
    $ pip install django-csp

::

    # source
    $ git clone https://github.com/mozilla/django-csp.git
    $ cd django-csp
    $ python setup.py install

Now edit your project's ``settings`` module, to add the django-csp middleware
to ``MIDDLEWARE``, like so::

    MIDDLEWARE = (
        # ...
        'csp.middleware.CSPMiddleware',
        # ...
    )
Note: Middleware order does not matter unless you have other middleware modifying the CSP header.

That should do it! Go on to :ref:`configuring CSP <configuration-chapter>`.

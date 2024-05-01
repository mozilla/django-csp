.. _installation-chapter:

=====================
Installing django-csp
=====================

First, install django-csp via pip or from source:

.. code-block:: bash

    pip install django-csp

Add the csp app to your ``INSTALLED_APPS`` in your project's ``settings`` module:

.. code-block:: python

    INSTALLED_APPS = (
        # ...
        "csp",
        # ...
    )

Now edit your project's ``settings`` module, to add the django-csp middleware
to ``MIDDLEWARE``, like so:

.. code-block:: python

    MIDDLEWARE = (
        # ...
        "csp.middleware.CSPMiddleware",
        # ...
    )

Note: Middleware order does not matter unless you have other middleware modifying the CSP header.

That should do it! Go on to :ref:`configuring CSP <configuration-chapter>`.

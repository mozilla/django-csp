.. _configuration-chapter:

======================
Configuring django-csp
======================

Content-Security-Policy_ is a complicated header. There are many values
you may need to tweak here.

.. note:
   Note when a setting requires a tuple or list. Since Python strings
   are iterable, you may get very strange policies and errors.

It's worth reading the latest CSP spec and making sure you understand it
before configuring django-csp.


Policy Settings
===============

These settings affect the policy in the header.

.. note:
   The "special" source values of ``'self'``, ``'unsafe-inline'``,
   ``'unsafe-eval'``, and ``'none'`` must be quoted! e.g.:
   ``CSP_DEFAULT_SRC = ("'self'",)``. Without quotes they will not work
   as intended.

:``CSP_DEFAULT_SRC``:
    Set the ``default-src`` directive. 

.. _Content-Security-Policy: http://www.w3.org/TR/CSP/

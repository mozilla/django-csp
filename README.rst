==========
Django-CSP
==========

Django-CSP adds Content-Security-Policy_ headers and a CSP report
processing facility to Django.

The code lives on GitHub_, where you can report Issues_. The full
documentation is available on ReadTheDocs_.

.. _Content-Security-Policy: http://www.w3.org/TR/CSP/
.. _GitHub: https://github.com/mozilla/django-csp
.. _Issues: https://github.com/mozilla/django-csp/issues
.. _ReadTheDocs: http://django-csp.readthedocs.org/


Using Django-CSP
================

Django-CSP is configured entirely in Django's settings. Almost all the
arguments take a tuple of possible values (cf the spec). Only the
``default-src`` directive has a default value (``'self'``). All others are
ignored unless specified.




The Settings
------------

These settings take a tuple of values. For simplicity, the special values
``'self'``, ``'unsafe-inline'``, and ``'unsafe-eval'`` must contain
the single quotes. See the spec for allowed use of the ``*`` wildcard::

    CSP_DEFAULT_SRC
    CSP_IMG_SRC
    CSP_SCRIPT_SRC
    CSP_STYLE_SRC
    CSP_OBJECT_SRC
    CSP_MEDIA_SRC
    CSP_FRAME_SRC
    CSP_FONT_SRC
    CSP_CONNECT_SRC
    CSP_SANDBOX

The following settings take only a URI, not a tuple::

    CSP_REPORT_URI

You can disable CSP for specific url prefixes with the
``CSP_EXCLUDE_URL_PREFIXES`` setting. For example, to exclude the django admin
(which uses inline Javascript) with the standard urlconf::

    CSP_EXCLUDE_URL_PREFIXES = ('/admin',)




Report-Only Mode
----------------

Content Security Policy supports a *report-only* mode that will send
violation reports but not enforce the policy in the browser. This allows you
to test a site for compliance without potentially breaking anything for your
users.

To activate report-only mode, simply turn on ``CSP_REPORT_ONLY`` in
settings::

    CSP_REPORT_ONLY = True


Modifying the Policy
====================

Right now, the only way to modify the policy is with the ``@csp_exempt``
decorator::

    from csp.decorators import csp_exempt

    @csp_exempt
    def myview(request):
        return HttpResponse()

This will prevent the ``CSPMiddleware`` from sending any CSP headers from this
view.


TODO
====

* ``@csp_patch`` decorator that will allow you to patch a policy for a specific
  view. Will be... complicated.
* ``@csp_override`` decorator that allows you to replace a policy for a
  specific view.

.. [#] Strictly speaking, ``csp`` only needs to be in your installed apps
   if you plan to use the report feature.

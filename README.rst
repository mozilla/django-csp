==========
Django-CSP
==========

Django-CSP is a `Content Security Policy
<https://wiki.mozilla.org/Security/CSP/Specification>`_ implementation
for Django. It is implemented as middleware.


Using Django-CSP
================

Django-CSP is configured entirely in Django's settings. Almost all the
arguments take a tuple of possible values (cf the spec). Only the ``allow``
directive has a default value (``'self'``). All others are ignored unless
specified.


Turning on CSP
--------------

The simplest step is just turning on the middleware::

    MIDDLEWARE_CLASSES = (
        # ...
        'csp.middleware.CSPMiddleware',
        # ....
    )


The Settings
------------

These settings take a tuple of values. For simplicity, the special values
``'self'`` and ``'none'`` must contain the single quotes. See the spec for
allowed use of the ``*`` wildcard::

    CSP_ALLOW
    CSP_IMG_SRC
    CSP_SCRIPT_SRC
    CSP_STYLE_SRC
    CSP_OBJECT_SRC
    CSP_MEDIA_SRC
    CSP_FRAME_SRC
    CSP_FONT_SRC
    CSP_FRAME_ANCESTORS

The following settings take only a URI, not a tuple::

    CSP_REPORT_URI
    CSP_POLICY_URI


Report URI
----------

Content Security Policy allows you to specify a URI that accepts violation
reports. Django-CSP includes a view that accepts these reports and forwards
them via email to the list of people specified in the ``CSP_NOTIFY`` setting.

To accept violation reports, you need only add the following to your site's
``urls.py``::

    (r'^csp', include('csp.urls')),

Then set the ``CSP_REPORT_URI`` in ``settings.py`` accordingly::

    CSP_REPORT_URI = '/csp/report'

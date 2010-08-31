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


The Settings
------------

These settings take a tuple of values. For simplicity, the special values
``'self'`` and ``'none'`` must contain the single quotes. See the spec for
allowed use of the ``*`` wildcard.

    CSP_ALLOW
    CSP_IMG_SRC
    CSP_SCRIPT_SRC
    CSP_STYLE_SRC
    CSP_OBJECT_SRC
    CSP_MEDIA_SRC
    CSP_FRAME_SRC
    CSP_FONT_SRC
    CSP_FRAME_ANCESTORS

The following settings take only a URI, not a tuple.

    CSP_REPORT_URI
    CSP_POLICY_URI

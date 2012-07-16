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
        # ...
    )

and adding ``csp`` to your installed apps [#]_ ::

    INSTALLED_APPS = (
        # ...
        'csp',
        # ...
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
    CSP_XHR_SRC
    CSP_FRAME_ANCESTORS

The following settings take only a URI, not a tuple::

    CSP_REPORT_URI

You can disable CSP for specific url prefixes with the
``CSP_EXCLUDE_URL_PREFIXES`` setting. For example, to exclude the django admin
(which uses inline Javascript) with the standard urlconf::

    CSP_EXCLUDE_URL_PREFIXES = ('/admin',)


The Options Directive
^^^^^^^^^^^^^^^^^^^^^

Content Security Policy defines an ``options`` directive that allows you
to re-enable inline scripts and ``eval()``, both disabled by default when CSP
is active.

To re-enable both, for example, use the ``CSP_OPTIONS`` setting, a tuple::

    CSP_OPTIONS = ('inline-script', 'eval-script')

Or either ``inline-script`` or ``eval-script`` can be enabled separately.


Report URI
----------

Content Security Policy allows you to specify a URI that accepts
violation reports. Django-CSP includes a view that accepts these
reports, processes, and stores them. Reports are grouped according to a
herusitic combination, and if a new Group is recognized, Django-CSP will notify
by email, either by mailing the ``ADMINS`` list, or the list in the
``CSP_NOTIFY`` setting.

To accept violation reports, you need only add the following to your site's
``urls.py``::

    (r'^csp', include('csp.urls')),

Then set the ``CSP_REPORT_URI`` in ``settings.py`` accordingly::

    CSP_REPORT_URI = '/csp/report'


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

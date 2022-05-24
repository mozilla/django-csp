.. _decorator-chapter:

====================================
Modifying the Policy with Decorators
====================================

Content Security Policies should be restricted and paranoid by default.
You may, on some views, need to expand or change the policy. django-csp
includes four decorators to help.


``@csp_exempt``
===============

Using the ``@csp_exempt`` decorator disables the CSP header on a given
view.

::

    from csp.decorators import csp_exempt

    # Will not have a CSP header.
    @csp_exempt
    def myview(request):
        return render(...)

You can manually set this on a per-response basis by setting the
``_csp_exempt`` attribute on the response to ``True``::

    # Also will not have a CSP header.
    def myview(request):
        response = render(...)
        response._csp_exempt = True
        return response


``@csp_update``
===============

The ``@csp_update`` header allows you to **append** values to the source
lists specified in the settings. If there is no setting, the value
passed to the decorator will be used verbatim.

.. note::
   To quote the CSP spec: "There's no inheritance; ... the default list
   is not used for that resource type" if it is set. E.g., the following
   will not allow images from 'self'::

    default-src 'self'; img-src imgsrv.com

The arguments to the decorator the same as the :ref:`settings
<configuration-chapter>` without the ``CSP_`` prefix, e.g. ``IMG_SRC``.
(They are also case-insensitive.) The values are either strings, lists
or tuples.

::

    from csp.decorators import csp_update

    # Will allow images from imgsrv.com.
    @csp_update(IMG_SRC='imgsrv.com')
    def myview(request):
        return render(...)


``@csp_replace``
================

The ``@csp_replace`` decorator allows you to **replace** a source list
specified in settings. If there is no setting, the value passed to the
decorator will be used verbatim. (See the note under ``@csp_update``.)

The arguments and values are the same as ``@csp_update``
::

    from csp.decorators import csp_replace

    # settings.CSP_IMG_SRC = ['imgsrv.com']
    # Will allow images from imgsrv2.com, but not imgsrv.com.
    @csp_replace(IMG_SRC='imgsrv2.com')
    def myview(request):
        return render(...)


``@csp_select``
===============

The ``@csp_select`` decorator allows you to select policies to include
from the current policy definitions being applied.

It accepts a mixed iterable of names or indices into the compiled definitions.

It acts very much like the ``CSP_POLICIES`` setting except that it can use
indices, which don't work for ``CSP_POLICIES`` because it's used to define
the order on the compiled policy in the first place).

NOTE: in the case of passing a ``dict`` to one of the other decorators,
the order will not be well-defined before Python 3.6.
Avoid using indices in this cases.

For named policies it will fallback to ``CSP_POLICY_DEFINITIONS`` even if they
don't appear in the current policy, so use with care
::
    from csp.decorators import csp_select

    # Using default settings
    # Will first apply the default policy, then the second policy, then the first policy
    @csp_select(['default', 1, 0])  # or @csp_select(['default', 'second', 'first])
    @csp(csp_definitions=(
        ('first', {'default-src': ["'self'"], 'img-src': ['imgsrv.com']}),
        ('second', {'script-src': ['scriptsrv.com', 'googleanalytics.com']},
    ))
    def myview(request):
        return render(...)


``@csp``
========

If you need to set the entire policy on a view, ignoring all the
settings, you can use the ``@csp`` decorator. The arguments and values
are as above
::

    from csp.decorators import csp

    @csp(DEFAULT_SRC=["'self'"], IMG_SRC=['imgsrv.com'],
         SCRIPT_SRC=['scriptsrv.com', 'googleanalytics.com'])
    def myview(request):
        return render(...)

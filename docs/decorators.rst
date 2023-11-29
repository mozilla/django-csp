.. _decorator-chapter:

====================================
Modifying the Policy with Decorators
====================================

Content Security Policies should be restricted and paranoid by default.
You may, on some views, need to expand or change the policy. django-csp
includes four decorators to help.


.. _csp-exempt-decorator:

``@csp_exempt``
===============

Using the ``@csp_exempt`` decorator disables the CSP headers on a given
view.

::

    from csp.decorators import csp_exempt

    # Will not have CSP headers.
    @csp_exempt
    def myview(request):
        return render(...)

You can manually set this on a per-response basis by setting the
``_csp_exempt`` attribute on the response to ``True``::

    # Also will not have CSP headers.
    def myview(request):
        response = render(...)
        response._csp_exempt = True
        return response


.. _csp-select-decorator:

``@csp_select``
===============

The ``@csp_select`` decorator allows you to select policies to include
from the current policy definitions, including those added
through the ``@csp`` :ref:`decorator <csp-decorator>` or the
``@csp_append`` :ref:`decorator <csp-append-decorator>` and those
defined in ``CSP_POLICY_DEFINITIONS``.

The arguments are positional-only names of policies.

It effectively overrides the ``CSP_POLICIES`` setting for a single view.
::

    from csp.decorators import csp_select

    # Will first apply the default policy and the alt second policy.
    @csp_select('default', 'first')
    @csp({
        'alt': {
            'default-src': ["'self'"],
            'img-src': ['imgsrv.com'],
            'report-only': True,
        },
    })
    def myview(request):
        return render(...)


.. _csp-update-decorator:

``@csp_update``
===============

The ``@csp_update`` decorator allows you to **append** values to the source
lists specified in a policy. If there is no setting, the value
passed to the decorator will be used verbatim. There are two different
parameter formats:

1. Keyword arguments that are the uppercased CSP directives, with dashes
replaced by underscores (the same as the :ref:`deprecated-policy-settings`
without the ``CSP_`` prefix, but case-insensitive). The values are either
strings, lists or tuples. In this mode of calling there is an optional
positional argument specifying which named policies to which to apply the
directives (default: ``('default',)``).
::

    from csp.decorators import csp_update

    # Will allow images from imgsrv.com in the default policy.
    @csp_update(IMG_SRC='imgsrv.com')
    def myview(request):
        return render(...)

2. Keyword arguments that are named policies equivalent to the format of
``CSP_POLICY_DEFINITIONS``.
::

    from csp.decorators import csp_update

    # Will allow images from imgsrv.com in the default policy.
    @csp_update(default={'img-src': 'imgsrv.com'})
    def myview(request):
        return render(...)

.. note::
   To quote the CSP spec: "There's no inheritance; ... the default list
   is not used for that resource type" if it is set. E.g., the following
   will not allow images from 'self'::

    default-src 'self'; img-src imgsrv.com


.. _csp-replace-decorator:


``@csp_replace``
================

The ``@csp_replace`` decorator allows you to **replace** a source list
specified in a policy. Setting a directive to ``None`` will delete that
directive from the policy. If there is no setting, the value passed to the
decorator will be used verbatim. See the note under
``@csp_update`` :ref:`decorator <csp-update-decorator>`.

The arguments and values are the same as ``@csp_update``
::

    from csp.decorators import csp_replace

    # settings.CSP_POLICY_DEFINITIONS = {'default': {'img-src': 'imgsrv.com'}}
    # Will allow images from imgsrv2.com, but not imgsrv.com.
    @csp_replace(IMG_SRC='imgsrv2.com')
    def myview(request):
        return render(...)

    # OR

    @csp_replace(default={'img-src': 'imgsrv2.com'})
    def myview(request):
        return render(...)


.. _csp-decorator:

``@csp``
========

If you need to replace the entire policy list on a view, ignoring all the
settings, you can use the ``@csp`` decorator.

The ``@csp_select`` :ref:`decorator <csp-select-decorator>` can be used to
combine these with the policies configured in ``CSP_POLICY_DEFINITIONS``
(but see also the ``@csp_append`` :ref:`decorator <csp-append-decorator>` below).

The arguments and values are the same as the ``@csp_update``
:ref:`decorator <csp-update-decorator>` except that it accepts optional position
arguments that are unnamed policies.
::

    from csp.decorators import csp

    @csp(
        DEFAULT_SRC=["'self'"],
        IMG_SRC=['imgsrv.com'],
        SCRIPT_SRC=['scriptsrv.com', 'googleanalytics.com'],
    )
    def myview(request):
        return render(...)

    # OR

    @csp(new={
        default-src=["'self'"],
        img-src=['imgsrv.com'],
        script-src=['scriptsrv.com', 'googleanalytics.com'],
    })
    def myview(request):
        return render(...)

    # OR

    @csp({
        default-src=["'self'"],
        img-src=['imgsrv.com'],
        script-src=['scriptsrv.com', 'googleanalytics.com'],
    })
    def myview(request):
        return render(...)


.. _csp-append-decorator:

``@csp_append``
===============

The ``@csp_append`` decorator allows you to add a new policy to
the policies configured in settings to a view.

The arguments and values are the same as the ``@csp``
:ref:`decorator <csp-decorator>`.
::

    from csp.decorators import csp_append

    # Add this stricter policy as report_only for myview.
    @csp_append({
        default-src=["'self'"],
        img-src=['imgsrv.com'],
        script-src=['scriptsrv.com', 'googleanalytics.com'],
        report_only=True,
    })
    def myview(request):
        return render(...)

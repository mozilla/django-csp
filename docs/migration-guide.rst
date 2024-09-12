.. _migration-guide-chapter:

==============================
django-csp 4.0 Migration Guide
==============================

Overview
========

In the latest version of `django-csp`, the format for configuring Content Security Policy (CSP)
settings has been updated are are backwards-incompatible with prior versions. The previous approach
of using individual settings prefixed with ``CSP_`` for each directive is no longer supported.
Instead, all CSP settings are now consolidated into one of two dict-based settings:
``CONTENT_SECURITY_POLICY`` or ``CONTENT_SECURITY_POLICY_REPORT_ONLY``.

Migrating from the Old Settings Format
======================================

Update `django-csp`
-------------------

First, update the `django-csp` package to the latest version that supports the new settings format.
You can do this by running:

.. code-block:: bash

    pip install -U django-csp

Add the `csp` app to `INSTALLED_APPS`
-------------------------------------

In your Django project's `settings.py` file, add the `csp` app to the ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        "csp",
        # ...
    ]

Run the Django check command
----------------------------

This is optional but can help kick start the new settings configuration for you. Run the Django
check command which will look for old settings and output a configuration in the new format:

.. code-block:: bash

    python manage.py check

This can help you identify the existing CSP settings in your project and provide a starting point
for migrating to the new format.

Identify Existing CSP Settings
------------------------------

Locate all the existing CSP settings in your Django project. These settings start with the
``CSP_`` prefix, such as ``CSP_DEFAULT_SRC``, ``CSP_SCRIPT_SRC``, ``CSP_IMG_SRC``, etc.

Create the New Settings Dictionary
----------------------------------

In your Django project's `settings.py` file, create a new dictionary called
``CONTENT_SECURITY_POLICY`` or ``CONTENT_SECURITY_POLICY_REPORT_ONLY``, depending on whether you want to
enforce the policy or only report violations, or both. Use the output from the Django check command
as a starting point to populate this dictionary.

Migrate Existing Settings
-------------------------

Migrate your existing CSP settings to the new format by populating the ``DIRECTIVES`` dictionary
inside the ``CONTENT_SECURITY_POLICY`` setting. The keys of the ``DIRECTIVES`` dictionary should be the
CSP directive names in lowercase, and the values should be lists containing the corresponding
sources. The Django check command output can help you identify the directive names and sources.

For example, if you had the following old settings:

.. code-block:: python

    CSP_DEFAULT_SRC = ["'self'", "*.example.com"]
    CSP_SCRIPT_SRC = ["'self'", "js.cdn.com/example/"]
    CSP_IMG_SRC = ["'self'", "data:", "example.com"]
    CSP_EXCLUDE_URL_PREFIXES = ["/admin"]

The new settings would be:

.. code-block:: python

    from csp.constants import SELF

    CONTENT_SECURITY_POLICY = {
        "EXCLUDE_URL_PREFIXES": ["/admin"],
        "DIRECTIVES": {
            "default-src": [SELF, "*.example.com"],
            "script-src": [SELF, "js.cdn.com/example/"],
            "img-src": [SELF, "data:", "example.com"],
        },
    }

.. note::

    The keys in the ``DIRECTIVES`` dictionary, the directive names, are in lowercase and use dashes
    instead of underscores to match the CSP specification.

.. note::

    If you were using the ``CSP_INCLUDE_NONCE_IN`` setting, this has been removed in the new settings
    format.

    **Previously:** You could use the ``CSP_INCLUDE_NONCE_IN`` setting to specify which directives in
    your Content Security Policy (CSP) should include a nonce.

    **Now:** You can include a nonce in any directive by adding the ``NONCE`` constant from the
    ``csp.constants`` module to the list of sources for that directive.

    For example, if you had ``CSP_INCLUDE_NONCE_IN = ["script-src"]``, this should be updated to
    include the `NONCE` sentinel in the `script-src` directive values:

    .. code-block:: python

        from csp.constants import NONCE, SELF

        CONTENT_SECURITY_POLICY = {
            "DIRECTIVES": {
                "script-src": [SELF, NONCE],
                # ...
            },
        }

.. note::

    If you were using the ``CSP_REPORT_PERCENTAGE`` setting, this should be updated to be a float
    percentage between 0.0 and 100.0. For example, if you had ``CSP_REPORT_PERCENTAGE = 0.1``, this
    should be updated to ``10.0`` to represent 10% of CSP errors will be reported:

    .. code-block:: python

        CONTENT_SECURITY_POLICY = {
            "REPORT_PERCENTAGE": 10.0,
            "DIRECTIVES": {
                "report-uri": "/csp-report/",
                # ...
            },
        }

Remove Old Settings
-------------------

After migrating to the new settings format, remove all the old ``CSP_`` prefixed settings from your
`settings.py` file.

Update the CSP decorators
-------------------------

If you are using the CSP decorators in your views, those will need to be updated as well. The
decorators now accept a dictionary containing the CSP directives as an argument. For example:

.. code-block:: python

    from csp.decorators import csp_update


    @csp_update({"default-src": ["another-url.com"]})
    def my_view(request): ...

Additionally, each decorator now takes an optional ``REPORT_ONLY`` argument to specify whether the
policy should be enforced or only report violations. For example:

.. code-block:: python

    from csp.constants import SELF
    from csp.decorators import csp


    @csp({"default-src": [SELF]}, REPORT_ONLY=True)
    def my_view(request): ...

Due to the addition of the ``REPORT_ONLY`` argument and for consistency, the ``csp_exempt``
decorator now requires parentheses when used with and without arguments. For example:

.. code-block:: python

    from csp.decorators import csp_exempt


    @csp_exempt()
    @csp_exempt(REPORT_ONLY=True)
    def my_view(request): ...

Look for uses of the following decorators in your code: ``@csp``, ``@csp_update``, ``@csp_replace``,
and ``@csp_exempt``.

Migrating Custom Middleware
===========================
The `CSPMiddleware` has changed in order to support easier extension via subclassing.

The `CSPMiddleware.build_policy` and `CSPMiddleware.build_policy_ro` methods have been deprecated
in 4.0 and replaced with a new method `CSPMiddleware.build_policy_parts`.

.. note::
    The deprecated methods will be removed in 4.1.

Unlike the old methods, which returned the built CSP policy header string, `build_policy_parts`
returns a dataclass that can be modified and updated before the policy is built. This allows
custom middleware to modify the policy whilst inheriting behaviour from the base classes.

An existing custom middleware, such as this:

.. code-block:: python

    from django.http import HttpRequest, HttpResponseBase

    from csp.middleware import CSPMiddleware, PolicyParts


    class ACustomMiddleware(CSPMiddleware):

        def build_policy(self, request: HttpRequest, response: HttpResponseBase) -> str:
            config = getattr(response, "_csp_config", None)
            update = getattr(response, "_csp_update", None)
            replace = getattr(response, "_csp_replace", {})
            nonce = getattr(request, "_csp_nonce", None)

            # ... do custom CSP policy logic ...

            return build_policy(config=config, update=update, replace=replace, nonce=nonce)

        def build_policy_ro(self, request: HttpRequest, response: HttpResponseBase) -> str:
            config = getattr(response, "_csp_config_ro", None)
            update = getattr(response, "_csp_update_ro", None)
            replace = getattr(response, "_csp_replace_ro", {})
            nonce = getattr(request, "_csp_nonce", None)

            # ... do custom CSP report-only policy logic ...

            return build_policy(config=config, update=update, replace=replace, nonce=nonce)

can be replaced with this:

.. code-block:: python

    from django.http import HttpRequest, HttpResponseBase

    from csp.middleware import CSPMiddleware, PolicyParts


    class ACustomMiddleware(CSPMiddleware):

        def get_policy_parts(
            self,
            request: HttpRequest,
            response: HttpResponseBase,
            report_only: bool = False,
        ) -> PolicyParts:
            policy_parts = super().get_policy_parts(request, response, report_only)

            if report_only:
                ...  # do custom CSP report-only policy logic
            else:
                ...  # do custom CSP policy logic

            return policy_parts

Conclusion
==========

By following this migration guide, you should be able to successfully update your Django project to
use the new dict-based CSP settings format introduced in the latest version of `django-csp`. This
change aligns the package with the latest CSP specification and provides a more organized and
flexible way to configure your Content Security Policy.

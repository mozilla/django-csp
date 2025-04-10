.. _configuration-chapter:

======================
Configuring django-csp
======================

Content-Security-Policy_ is a complicated header. There are many values
you may need to tweak here.

It's worth reading the latest CSP spec_ and making sure you understand it
before configuring django-csp.

.. note::
   Many settings require a ``tuple`` or ``list``. You may get very strange
   policies and even errors when mistakenly configuring them as a ``string``.


Migrating from django-csp <= 3.8
================================

Version 4.0 of django-csp introduces a new configuration format that breaks compatibility with
previous versions.  If you are migrating from django-csp 3.8 or lower, you will need to update your
settings to the new format. See the :ref:`migration guide <migration-guide-chapter>` for more
information.

Configuration
=============

All configuration of django-csp is done in your Django settings file with the
``CONTENT_SECURITY_POLICY`` setting or the ``CONTENT_SECURITY_POLICY_REPORT_ONLY`` setting. Each of these
settings expects a dictionary representing a policy.

The ``CONTENT_SECURITY_POLICY`` setting is your enforceable policy.

The ``CONTENT_SECURITY_POLICY_REPORT_ONLY`` setting is your report-only policy. This policy is
used to test the policy without breaking the site. It is useful when setting this policy to be
slightly more strict than the default policy to see what would be blocked if the policy was enforced.

The following is an example of a policy configuration with a default policy and a report-only
policy. The default policy is considered a "relaxed" policy that allows for the most flexibility
while still providing a good level of security. The report-only policy is considered a step towards
a more slightly strict policy and is used to test the policy without breaking the site.

.. code-block:: python

    from csp.constants import NONE, SELF

    CONTENT_SECURITY_POLICY = {
        "EXCLUDE_URL_PREFIXES": ["/excluded-path/"],
        "DIRECTIVES": {
            "default-src": [SELF, "cdn.example.net"],
            "frame-ancestors": [SELF],
            "form-action": [SELF],
            "report-uri": "/csp-report/",
        },
    }

    CONTENT_SECURITY_POLICY_REPORT_ONLY = {
        "EXCLUDE_URL_PREFIXES": ["/excluded-path/"],
        "DIRECTIVES": {
            "default-src": [NONE],
            "connect-src": [SELF],
            "img-src": [SELF],
            "form-action": [SELF],
            "frame-ancestors": [SELF],
            "script-src": [SELF],
            "style-src": [SELF],
            "upgrade-insecure-requests": True,
            "report-uri": "/csp-report/",
        },
    }

.. note::

    In the above example, the constant ``NONE`` is converted to the CSP keyword ``"'none'"`` and
    is distinct from Python's ``None`` value. The CSP keyword ``'none'`` is a special value that
    signifies that you do not want any sources for this directive. The ``None`` value is a
    Python keyword that represents the absence of a value and when used as the value of a directive,
    it will remove the directive from the policy.

    This is useful when using the ``@csp_replace`` decorator to effectively clear a directive from
    the base configuration as defined in the settings. For example, if the Django settings the
    ``frame-ancestors`` directive is set to a list of sources and you want to remove the
    ``frame-ancestors`` directive from the policy for this view:

    .. code-block:: python

        from csp.decorators import csp_replace


        @csp_replace({"frame-ancestors": None})
        def my_view(request): ...


Policy Settings
===============

At the top level of the policy dictionary, these are the keys that can be used to configure the
policy.

``EXCLUDE_URL_PREFIXES``
    A ``tuple`` or ``list`` of URL prefixes to exclude from CSP protection. URLs beginning with any
    of these strings will not get the Content-Security-Policy response headers at all.

    .. warning::

       Excluding any path on your site will eliminate the benefits of CSP everywhere on your site.
       The typical browser security model for JavaScript considers all paths alike. A Cross-Site
       Scripting flaw on, e.g., ``excluded-page/`` can therefore be leveraged to access everything
       on the same origin.

``REPORT_PERCENTAGE``
    Percentage of requests that should see the ``report-uri`` directive.  Use this to throttle the
    number of CSP violation reports made to your ``report-uri``. A **float** between 0.0 and 100.0
    (0.0 = no reports at all, 100.0 = always report).  Ignored if ``report-uri`` isn't set.

    .. note::
       To allow rate limiting, ``csp.contrib.rate_limiting.RateLimitedCSPMiddleware`` must be used
       instead of ``csp.middleware.CSPMiddleware``.
       See :ref:`violation reporting <reports-chapter>` for more details.

``DIRECTIVES``
    A dictionary of policy directives. Each key in the dictionary is a directive and the value is a
    list of sources for that directive. The following is a list of all the directives that can be
    configured.

    .. note::

       The CSP keyword values of ``'self'``, ``'unsafe-inline'``, ``'strict-dynamic'``, etc. must be
       quoted!  e.g.: ``"default-src": ["'self'"]``.  Without quotes they will not work as intended.

       New in version 4.0 are CSP keyword constants. Use these to minimize quoting mistakes and typos.

       The following CSP keywords are available:

           * ``NONE`` = ``"'none'"``
           * ``REPORT_SAMPLE`` = ``"'report-sample'"``
           * ``SELF`` = ``"'self'"``
           * ``STRICT_DYNAMIC`` = ``"'strict-dynamic'"``
           * ``UNSAFE_ALLOW_REDIRECTS`` = ``"'unsafe-allow-redirects'"``
           * ``UNSAFE_EVAL`` = ``"'unsafe-eval'"``
           * ``UNSAFE_HASHES`` = ``"'unsafe-hashes'"``
           * ``UNSAFE_INLINE`` = ``"'unsafe-inline'"``
           * ``WASM_UNSAFE_EVAL`` = ``"'wasm-unsafe-eval'"``

       Example usage:

       .. code-block:: python

            from csp.constants import NONE, SELF, STRICT_DYNAMIC

            CONTENT_SECURITY_POLICY = {
                "DIRECTIVES": {
                    # No sources allowed for default-src by using `csp.constants.NONE`.
                    "default-src": [NONE],
                    "script-src": [SELF, STRICT_DYNAMIC],
                    "style-src": [SELF],
                    # Using Python's `None` will not include the directive in the header. Useful
                    # to override previous settings or when using the decorators.
                    "base-uri": None,
                }
            }

    .. note::
       The CSP keyword ``csp.constants.NONE`` is distinct from Python's ``None`` value. The CSP
       keyword ``'none'`` is a special value that signifies that you do not want any sources for
       the directive. The ``None`` value is a Python keyword that represents the absence of a value
       and when used as the value of a directive, it will remove the directive from the header.

    .. note::
       Deprecated features of CSP in general have been moved to the bottom of this list.

    .. warning::
       The ``'unsafe-inline'`` and ``'unsafe-eval'`` sources are considered harmful and should be
       avoided. They are included here for completeness, but should not be used in production.

    ``default-src``
        Set the ``default-src`` directive. A ``tuple`` or ``list`` of values,
        e.g.: ``("'self'", "cdn.example.net")``. *default=["'self'"]*

    ``script-src``
        Set the ``script-src`` directive. A ``tuple`` or ``list``. *default=None*

    ``script-src-attr``
        Set the ``script-src-attr`` directive. A ``tuple`` or ``list``. *default=None*

    ``script-src-elem``
        Set the ``script-src-elem`` directive. A ``tuple`` or ``list``. *default=None*

    ``img-src``
        Set the ``img-src`` directive. A ``tuple`` or ``list``. *default=None*

    ``object-src``
        Set the ``object-src`` directive. A ``tuple`` or ``list``. *default=None*

    ``media-src``
        Set the ``media-src`` directive. A ``tuple`` or ``list``. *default=None*

    ``frame-src``
        Set the ``frame-src`` directive. A ``tuple`` or ``list``. *default=None*

    ``font-src``
        Set the ``font-src`` directive. A ``tuple`` or ``list``. *default=None*

    ``connect-src``
        Set the ``connect-src`` directive. A ``tuple`` or ``list``. *default=None*

    ``style-src``
        Set the ``style-src`` directive. A ``tuple`` or ``list``. *default=None*

    ``style-src-attr``
        Set the ``style-src-attr`` directive. A ``tuple`` or ``list``. *default=None*

    ``style-src-elem``
        Set the ``style-src-elem`` directive. A ``tuple`` or ``list``. *default=None*

    ``base-uri``
        Set the ``base-uri`` directive. A ``tuple`` or ``list``. *default=None*

        Note: This doesn't use ``default-src`` as a fall-back.

    ``child-src``
        Set the ``child-src`` directive. A ``tuple`` or ``list``. *default=None*

    ``frame-ancestors``
        Set the ``frame-ancestors`` directive. A ``tuple`` or ``list``. *default=None*

        Note: This doesn't use ``default-src`` as a fall-back.

    ``navigate-to``
        Set the ``navigate-to`` directive. A ``tuple`` or ``list``. *default=None*

        Note: This doesn't use ``default-src`` as a fall-back.

    ``form-action``
        Set the ``form-action`` directive. A ``tuple`` or ``list``. *default=None*

        Note: This doesn't use ``default-src`` as a fall-back.

    ``sandbox``
        Set the ``sandbox`` directive. A ``tuple`` or ``list``. *default=None*

        Note: This doesn't use ``default-src`` as a fall-back.

    ``report-uri``
        Set the ``report-uri`` directive. A ``tuple`` or ``list`` of URIs.
        Each URI can be a full or relative URI. *default=None*

        Note: This doesn't use ``default-src`` as a fall-back.

    ``report-to``
        Set the ``report-to`` directive. A ``string`` describing a reporting
        group. *default=None*

        See Section 1.2: https://w3c.github.io/reporting/#group

        Also `see this MDN note on <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/report-uri>`_ ``report-uri`` and ``report-to``.

    ``manifest-src``
        Set the ``manifest-src`` directive. A ``tuple`` or ``list``. *default=None*

    ``worker-src``
        Set the ``worker-src`` directive. A ``tuple`` or ``list``. *default=None*

    ``require-sri-for``
        Set the ``require-sri-for`` directive. A ``tuple`` or ``list``. *default=None*

        Valid values: a ``list`` containing ``'script'``, ``'style'``, or both.

        Spec: require-sri-for-known-tokens_

    ``upgrade-insecure-requests``
        Include ``upgrade-insecure-requests`` directive. A ``boolean``. *default=False*

        Spec: upgrade-insecure-requests_

    ``require-trusted-types-for``
        Include ``require-trusted-types-for`` directive. A ``tuple`` or ``list``. *default=None*

        Valid values: ``["'script'"]``

    ``trusted-types``
        Include ``trusted-types`` directive. A ``tuple`` or ``list``. *default=None*

        Valid values: a ``list`` of allowed policy names that may include
        ``default`` and/or ``'allow-duplicates'``


Deprecated CSP settings
-----------------------
The following ``DIRECTIVES`` settings are still configurable, but are considered deprecated
in terms of the latest implementation of the relevant spec.


``block-all-mixed-content``
    Include ``block-all-mixed-content`` directive. A ``boolean``. *default=False*

    Related `note on MDN <block-all-mixed-content_mdn_>`_.

    Spec: block-all-mixed-content_


``plugin-types``
    Set the ``plugin-types`` directive. A ``tuple`` or ``list``. *default=None*

    Note: This doesn't use ``default-src`` as a fall-back.

    Related `note on MDN <plugin_types_mdn_>`_.


``prefetch-src``
    Set the ``prefetch-src`` directive. A ``tuple`` or ``list``. *default=None*

    Related `note on MDN <prefetch_src_mdn_>`_.


Changing the Policy
~~~~~~~~~~~~~~~~~~~

The policy can be changed on a per-view (or even per-request) basis. See
the :ref:`decorator documentation <decorator-chapter>` for more details.


.. _Content-Security-Policy: https://www.w3.org/TR/CSP/
.. _Content-Security-Policy-L3: https://w3c.github.io/webappsec-csp/
.. _spec: Content-Security-Policy_
.. _require-sri-for-known-tokens: https://w3c.github.io/webappsec-subresource-integrity/#opt-in-require-sri-for
.. _upgrade-insecure-requests: https://w3c.github.io/webappsec-upgrade-insecure-requests/#delivery
.. _block-all-mixed-content: https://w3c.github.io/webappsec-mixed-content/
.. _block-all-mixed-content_mdn: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/block-all-mixed-content
.. _plugin_types_mdn: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/plugin-types
.. _prefetch_src_mdn: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/prefetch-src
.. _strict-csp: https://csp.withgoogle.com/docs/strict-csp.html

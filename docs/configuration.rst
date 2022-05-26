.. _configuration-chapter:

======================
Configuring django-csp
======================

Content-Security-Policy_ is a complicated header. There are many values
you may need to tweak here.

It's worth reading the latest CSP spec_ and making sure you understand it
before configuring django-csp.

Multiple policies can be configured using the below settings. There are two
reasons to do this:

1. To configure one policy as report-only and another to be enforced.

2. To have multiple policies enforced simultaneously for a directive, e.g
a ``{'include_nonce_in': ['default-src']}`` and ``{'default-src': ['self']}``.

Multiple policies for the same header will be separated by a ``,`` in the header.

.. note::
   Many directives require a ``tuple`` or ``list``. You may get very strange
   policies and even errors when mistakenly configuring them as a ``string``.


Policy Settings
===============

These settings affect the policy in the header. The defaults are in *italics*.

.. note::
   The "special" source values of ``'self'``, ``'unsafe-inline'``,
   ``'unsafe-eval'``, ``'none'`` and hash-source (``'sha256-...'``) must be
   quoted! e.g.: ``CSP_DEFAULT_SRC = ("'self'",)``. Without quotes they will
   not work as intended.

``CSP_POLICY_DEFINITIONS``
    A dictionary of dictionaries of directives or pseudo-directives. *{'default': default_policy}*

    `default_policy` uses the defaults for each directive as shown in :ref:`deprecated-policy-settings`
    and :ref:`deprecated-pseudo-directives` below.

    The policy directives are lower-case and use dashes (``-``) rather than (``_``) used by the
    :ref:`old settings<deprecated-policy-settings>`, with the exception of the
    :ref:`deprecated-pseudo-directives` (``report_only``, ``exclude_url_prefixes``, and
    ``include_nonce_in``) which are specified with underscores rather than dashes to distinguish
    them visually from the csp directives and for forwards compatibility.

``CSP_POLICIES``
    A list or tuple specifying which definitions will be applied by default and
    defining an order on those policies. *['default']*

    Note that not all policies defined in ``CSP_POLICY_DEFINITIONS`` need to be used here.  Those that
    aren't can be selected for a particular view using the ``@csp_select``
    :ref:`decorator <csp-select-decorator>`.


.. _deprecated-policy-settings:

Deprecated Policy Settings
--------------------------

With the introduction of multi-policy support, the following settings are deprecated.
If ``CSP_POLICY_DEFINITIONS`` is not defined, they will be used to populate it until
the deprecation period is over.  It will be populated with a single policy under the
``default`` key.

``CSP_DEFAULT_SRC``
    Set the ``default-src`` directive. A ``tuple`` or ``list`` of values,
    e.g.: ``("'self'", 'cdn.example.net')``. *["'self'"]*

``CSP_SCRIPT_SRC``
    Set the ``script-src`` directive. A ``tuple`` or ``list``. *None*

``CSP_SCRIPT_SRC_ATTR``
    Set the ``script-src-attr`` directive. A ``tuple`` or ``list``. *None*

``CSP_SCRIPT_SRC_ELEM``
    Set the ``script-src-elem`` directive. A ``tuple`` or ``list``. *None*

``CSP_IMG_SRC``
    Set the ``img-src`` directive. A ``tuple`` or ``list``. *None*

``CSP_OBJECT_SRC``
    Set the ``object-src`` directive. A ``tuple`` or ``list``. *None*

``CSP_PREFETCH_SRC``
    Set the ``prefetch-src`` directive. A ``tuple`` or ``list``. *None*

``CSP_MEDIA_SRC``
    Set the ``media-src`` directive. A ``tuple`` or ``list``. *None*

``CSP_FRAME_SRC``
    Set the ``frame-src`` directive. A ``tuple`` or ``list``. *None*

``CSP_FONT_SRC``
    Set the ``font-src`` directive. A ``tuple`` or ``list``. *None*

``CSP_CONNECT_SRC``
    Set the ``connect-src`` directive. A ``tuple`` or ``list``. *None*

``CSP_STYLE_SRC``
    Set the ``style-src`` directive. A ``tuple`` or ``list``. *None*

``CSP_STYLE_SRC_ATTR``
    Set the ``style-src-attr`` directive. A ``tuple`` or ``list``. *None*

``CSP_STYLE_SRC_ELEM``
    Set the ``style-src-elem`` directive. A ``tuple`` or ``list``. *None*

``CSP_BASE_URI``
    Set the ``base-uri`` directive. A ``tuple`` or ``list``. *None*

    Note: This doesn't use ``default-src`` as a fall-back.

``CSP_CHILD_SRC``
    Set the ``child-src`` directive. A ``tuple`` or ``list``. *None*

``CSP_FRAME_ANCESTORS``
    Set the ``frame-ancestors`` directive. A ``tuple`` or ``list``. *None*

    Note: This doesn't use ``default-src`` as a fall-back.

``CSP_NAVIGATE_TO``
    Set the ``navigate-to`` directive. A ``tuple`` or ``list``. *None*

    Note: This doesn't use ``default-src`` as a fall-back.

``CSP_FORM_ACTION``
    Set the ``FORM_ACTION`` directive. A ``tuple`` or ``list``. *None*

    Note: This doesn't use ``default-src`` as a fall-back.

``CSP_SANDBOX``
    Set the ``sandbox`` directive. A ``tuple`` or ``list``. *None*

    Note: This doesn't use ``default-src`` as a fall-back.

``CSP_REPORT_URI``
    Set the ``report-uri`` directive. A ``tuple`` or ``list`` of URIs.
    Each URI can be a full or relative URI. *None*

    Note: This doesn't use ``default-src`` as a fall-back.

``CSP_REPORT_TO``
    Set the ``report-to`` directive. A ``string`` describing a reporting
    group. *None*

    See Section 1.2: https://w3c.github.io/reporting/#group

``CSP_MANIFEST_SRC``
    Set the ``manifest-src`` directive. A ``tuple`` or ``list``. *None*

``CSP_WORKER_SRC``
    Set the ``worker-src`` directive. A ``tuple`` or ``list``. *None*

``CSP_PLUGIN_TYPES``
    Set the ``plugin-types`` directive. A ``tuple`` or ``list``. *None*

    Note: This doesn't use ``default-src`` as a fall-back.

``CSP_REQUIRE_SRI_FOR``
    Set the ``require-sri-for`` directive. A ``tuple`` or ``list``. *None*

    Valid values: a ``list`` containing ``'script'``, ``'style'``, or both.

    See: require-sri-for-known-tokens_

``CSP_UPGRADE_INSECURE_REQUESTS``
    Include ``upgrade-insecure-requests`` directive. A ``boolean``. *False*

    See: upgrade-insecure-requests_

``CSP_REQUIRE_TRUSTED_TYPES_FOR``
    Include ``require-trusted-types-for`` directive.
    A ``tuple`` or ``list``. *None*

    Valid values: ``["'script'"]``

``CSP_TRUSTED_TYPES``
    Include ``trusted-types`` directive.
    A ``tuple`` or ``list``. *None*

    Valid values: a ``list`` of allowed policy names that may include
    ``default`` and/or ``'allow-duplicates'``

``CSP_BLOCK_ALL_MIXED_CONTENT``
    Include ``block-all-mixed-content`` directive. A ``boolean``. *False*
    Note: Obsolete. All mixed content is now blocked if it can't be autoupgraded.
    See: block-all-mixed-content_


.. _deprecated-pseudo-directives:

Pseudo-Directives
^^^^^^^^^^^^^^^^^

These settings affect how the policy is applied, but do not correspond with a single
csp directive.

``CSP_INCLUDE_NONCE_IN``
    Include dynamically generated nonce in all listed directives.
    A ``tuple`` or ``list``, e.g.: ``CSP_INCLUDE_NONCE_IN = ['script-src']``
    will add ``'nonce-<b64-value>'`` to the ``script-src`` directive.
    *['default-src']*

    Note: The nonce value will only be generated if ``request.csp_nonce``
    is accessed during the request/response cycle.

``CSP_REPORT_ONLY``
    Send "report-only" headers instead of real headers.
    A ``boolean``. *False*

    See the spec_ and the chapter on :ref:`reports <reports-chapter>` for
    more info.

``CSP_EXCLUDE_URL_PREFIXES``
    A ``tuple`` (*not* a ``list``) of URL prefixes. URLs beginning with any
    of these will not get the CSP headers. *()*

.. warning::

   Excluding any path on your site will eliminate the benefits of CSP
   everywhere on your site. The typical browser security model for
   JavaScript considers all paths alike. A Cross-Site Scripting flaw
   on, e.g., ``excluded-page/`` can therefore be leveraged to access
   everything on the same origin.

Changing the Policy
-------------------

The policy can be changed on a per-view (or even per-request) basis. See
the :ref:`decorator documentation <decorator-chapter>` for more details.


.. _Content-Security-Policy: https://www.w3.org/TR/CSP/
.. _Content-Security-Policy-L3: https://w3c.github.io/webappsec-csp/
.. _spec: Content-Security-Policy_
.. _require-sri-for-known-tokens: https://w3c.github.io/webappsec-subresource-integrity/#opt-in-require-sri-for
.. _upgrade-insecure-requests: https://w3c.github.io/webappsec-upgrade-insecure-requests/#delivery
.. _block-all-mixed-content: https://w3c.github.io/webappsec-mixed-content/#strict-checking

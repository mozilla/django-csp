.. _configuration-chapter:

======================
Configuring django-csp
======================

Content-Security-Policy_ is a complicated header. There are many values
you may need to tweak here.

.. note::
   Note when a setting requires a tuple or list. Since Python strings
   are iterable, you may get very strange policies and errors.

It's worth reading the latest CSP spec and making sure you understand it
before configuring django-csp.


Policy Settings
===============

These settings affect the policy in the header. The defaults are in
*italics*.

.. note::
   The "special" source values of ``'self'``, ``'unsafe-inline'``,
   ``'unsafe-eval'``, and ``'none'`` must be quoted! e.g.:
   ``CSP_DEFAULT_SRC = ("'self'",)``. Without quotes they will not work
   as intended.

``CSP_DEFAULT_SRC``
    Set the ``default-src`` directive. A tuple or list of
    values, e.g. ``("'self'", 'cdn.example.net')``. *'self'*
``CSP_SCRIPT_SRC``
    Set the ``script-src`` directive. A tuple or list. *None*
``CSP_IMG_SRC``
    Set the ``img-src`` directive. A tuple or list. *None*
``CSP_OBJECT_SRC``
    Set the ``object-src`` directive. A tuple or list. *None*
``CSP_MEDIA_SRC``
    Set the ``media-src`` directive. A tuple or list. *None*
``CSP_FRAME_SRC``
    Set the ``frame-src`` directive. A tuple or list. *None*
``CSP_FONT_SRC``
    Set the ``font-src`` directive. A tuple or list. *None*
``CSP_CONNECT_SRC``
    Set the ``connect-src`` directive. A tuple or list. *None*
``CSP_STYLE_SRC``
    Set the ``style-src`` directive. A tuple or list. *None*
``CSP_BASE_URI``
    Set the ``base-uri`` directive. A tuple or list. *None*
    Note: This doesn't use default-src as a fall-back.
``CSP_CHILD_SRC``
    Set the ``child-src`` directive. A tuple or list. *None* Note: Deprecated in CSP v3. Use frame-src and worker-src instead.
``CSP_FRAME_ANCESTORS``
    Set the ``FRAME_ANCESTORS`` directive. A tuple or list. *None*
    Note: This doesn't use default-src as a fall-back.
``CSP_FORM_ACTION``
    Set the ``FORM_ACTION`` directive. A tuple or list. *None*
    Note: This doesn't use default-src as a fall-back.
``CSP_SANDBOX``
    Set the ``sandbox`` directive. A tuple or list. *None*
    Note: This doesn't use default-src as a fall-back.
``CSP_REPORT_URI``
    Set the ``report-uri`` directive. A tuple or list. Each URI can be a
    full or relative URI. *None*
    Note: This doesn't use default-src as a fall-back.
``CSP_MANIFEST_SRC``
    Set the ``manifest-src`` directive. A tuple or list. *None*
``CSP_WORKER_SRC``
    Set the ``worker-src`` directive. A tuple or list. *None*
``CSP_PLUGIN_TYPES``
    Set the ``plugin-types`` directive. A tuple or list. *None*
    Note: This doesn't use default-src as a fall-back.
``CSP_REQUIRE_SRI_FOR``
    Set the ``require-sri-for`` directive. A tuple or list. *None*
    Valid values: ``script``, ``style``, or both. See: require-sri-for-known-tokens_
    Note: This doesn't use default-src as a fall-back.
``CSP_UPGRADE_INSECURE_REQUESTS``
    Include ``upgrade-insecure-requests`` directive. A boolean. *False*
    See: upgrade-insecure-requests_
``CSP_BLOCK_ALL_MIXED_CONTENT``
    Include ``block-all-mixed-content`` directive. A boolean. *False*
    See: block-all-mixed-content_
``CSP_INCLUDE_NONCE_IN``
    Include dynamically generated nonce in all listed directives, e.g. ``CSP_INCLUDE_NONCE_IN=['script-src']`` will add ``'nonce-<b64-value>'`` to the ``script-src`` directive. A tuple or list. *None*


Changing the Policy
-------------------

The policy can be changed on a per-view (or even per-request) basis. See
the :ref:`decorator documentation <decorator-chapter>` for more details.


Other Settings
==============

These settings control the behavior of django-csp. Defaults are in
*italics*.

``CSP_REPORT_ONLY``
    Send "report-only" headers instead of real headers. See the spec_
    and the chapter on :ref:`reports <reports-chapter>` for more info. A
    boolean. *False*
``CSP_EXCLUDE_URL_PREFIXES``
    A **tuple** of URL prefixes. URLs beginning with any of these will
    not get the CSP headers. *()*

.. warning::

   Excluding any path on your site will eliminate the benefits of CSP
   everywhere on your site. The typical browser security model for
   JavaScript considers all paths alike. A Cross-Site Scripting flaw
   on, e.g., `excluded-page/` can therefore be leveraged to access everything
   on the same origin.

.. _Content-Security-Policy: http://www.w3.org/TR/CSP/
.. _spec: Content-Security-Policy_
.. _require-sri-for-known-tokens: https://w3c.github.io/webappsec-subresource-integrity/#opt-in-require-sri-for
.. _upgrade-insecure-requests: https://w3c.github.io/webappsec-upgrade-insecure-requests/#delivery
.. _block-all-mixed-content: https://w3c.github.io/webappsec-mixed-content/

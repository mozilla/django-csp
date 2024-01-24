===================================
Implementing Trusted Types with CSP
===================================

``DOM Cross-site Scripting``
============================
Cross-site scripting (XSS) is one of the most prevalent vulnerabilities
on the web. Nonce-based CSP is used to prevent server-side XSS. Trusted
Types are used to prevent client-side or DOM-XSS_. Trusted Types rely on
the browser to enforce the policy that is provided to it. Currently, Trusted
Types are supported on Chrome 83 and Android Webview. Many browsers are in the
process of adding support. Check back for updated compatibility_.

Follow the simple steps below to make your web application Trusted Types
compliant.


``Step 1: Enable Trusted Types and Report Only Mode``
=====================================================
Trusted Types require data to be processed before being sent to a risky "sink" where DOM XSS might occur, such as when assigning to Element.innerHTML or calling document.write. When enforced, Trusted Types will tell the
browser to block any data that is not properly processed. In order to avoid
this, you must fix offending parts of your code. To see where adjustments will
be required, turn on trusted types and report only mode.

Configure django-csp so that ``CSP_REQUIRE_TRUSTED_TYPES_FOR`` is set to *‘script’*.

Configure django-csp so that ``CSP_REPORT_ONLY`` is set to *True*.

Configure django-csp so that ``CSP_REPORT_URI`` is set to an app or CSP report processing service that you control.

Now trusted types violations will be reported to your ``CSP_REPORT_URI`` without blocking any of your application’s functionalities.


``Step 2: Fixing Trusted Types Violations``
===========================================
There are four ways to resolve trusted types violations. They are explained
here in order of preference.

Rewrite the Code
----------------
It may be possible for your code to be rewritten without using dangerous
functions. For example, instead of dynamically placing an image using the
dangerous ``innerHTML`` sink, the image could be created with
``document.createElement`` and placed using the ``appendChild`` function.

Rewriting may be possible for any of the dangerous sinks, which are listed here.

* Script manipulation:
    * ``<script src>`` and setting text content of ``<script>`` elements.
        * Tip: Avoid creating scripts at run time
        * Tip: Create a policy with a URL stringifier to verify scripts are from a trusted origin
* Generating HTML from a string:
    * ``innerHTML``, ``outerHTML``, ``insertAdjacentHTML``, ``<iframe> srcdoc``, ``document.write``, ``document.writeln``, and ``DOMParser.parseFromString``
        * Tip: Use textContent instead of inner HTML
        * Tip: Use a templating library that supports Trusted Types
        * Tip: Use createElement and appendChild as explained above
* Executing plugin content:
    * ``<embed src>``, ``<object data>`` and ``<object codebase>``
        * Tip: Consider limiting plugin content by setting``CSP_OBJECT_SRC`` to *none*
* Runtime JavaScript code compilation:
    * ``eval``, ``setTimeout``, ``setInterval``, and ``new Function()``
        * Tip: Avoid using eval entirely
        * Tip: Avoid passing strings to runtime compiled functions

Use a Library
-------------
When code cannot be rewritten to avoid dangerous sinks, Trusted Types require
that data be processed before being passed to a dangerous sink. Processed data
is wrapped in a TrustedHTML, TrustedScript, or TrustedScriptURL object to certify that
it has been sanitized or otherwise assured to be safe in the given context. Some libraries will process data and return Trusted
Types objects for you. For example, DOMPurify_ supports Trusted Types.

.. note::
   Libraries are preferred to writing your own sanitation policies since they
   are generally more comprehensive, secure, and well reviewed.

Create Trusted Types Policies
-----------------------------
Where code cannot be rewritten and an existing library cannot be used, you will
have to create Trusted Types objects yourself. This is done using policies. Different policies can be created for use in different contexts.
Policies produce Trusted Types after enforcing security rules on their input
based on the sink context. Each policy should be given a distinct name.

Here is an example policy that sanitizes HTML by escaping the ``<`` character.

.. code-block:: javascript

	if (window.trustedTypes && trustedTypes.createPolicy) {
    	const escapeHTMLPolicy = trustedTypes.createPolicy('myEscapePolicy', {
    		createHTML: string => string.replace(/\</g, '&lt;')
  		});
	}

Here is an example of how that policy can be used.

.. code-block:: javascript

	const escaped = escapeHTMLPolicy.createHTML('<img src=x onerror=alert(1)>');
	console.log(escaped instanceof TrustedHTML);
	el.innerHTML = escaped;

.. note::
   Keep in mind that you are creating your own security rules with policies.
   Your application is only protected from DOM XSS if you use strict sanitation
   rules that consider which sink is accepting the data.

Use a Default Policy
--------------------
In the event that you don’t have control over the offending code, you can use a
default policy. This may happen if you are loading a third party library that
is not Trusted Types compliant. A default policy is defined the same way as any
other Trusted Types policy. In order to be used by the browser as the default
policy it must be named *default*.

The policy called *default* will be used wherever a string is sent to a
dangerous sink that requires Trusted Types.


``Step 3: Enforce Trusted Types``
=================================
Once you have addressed all of the Trusted Types violations present in your
application, you can begin enforcing Trusted Types to prevent DOM XSS.

Configure django-csp so that ``CSP_REPORT_ONLY`` is set to *False*.

.. note::
   To learn more about trusted types or learn how to limit policy creation with
   ``CSP_TRUSTED_TYPES`` take a look at the complete spec_ or the article_ this
   guide is based on.



.. _DOM-XSS: https://owasp.org/www-community/attacks/xss/
.. _compatibility: https://developer.mozilla.org/es/docs/Web/HTTP/Headers/Content-Security-Policy/trusted-types#Browser_compatibility
.. _DOMPurify: https://github.com/cure53/DOMPurify#what-about-dompurify-and-trusted-types
.. _spec: https://w3c.github.io/webappsec-trusted-types/dist/spec/
.. _article: https://web.dev/trusted-types/

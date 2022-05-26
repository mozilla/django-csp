==============================
Using the generated CSP nonce
==============================
When ``CSP_INCLUDE_NONCE_IN`` is configured, the nonce value is returned in the CSP headers **if it is used**.
To actually make the browser do anything with this value, you will need to include it in the attributes of
the tags that you wish to mark as safe.


.. Note::

   Use view source on a page to see nonce values. **Nonce values are
   not visible in browser developer tools.** To prevent malicious CSS
   selectors leaking the values, `they are not exposed to the DOM
   <https://github.com/whatwg/html/pull/2373>`_.


``Middleware``
==============
Installing the middleware creates a lazily evaluated property ``csp_nonce`` and attaches it to all incoming requests.

.. code-block:: python

	MIDDLEWARE_CLASSES = (
    	#...
    	'csp.middleware.CSPMiddleware',
    	#...
    )

This value can be accessed directly on the request object in any view or template and manually appended to any script element like so -

.. code-block:: html

	<script nonce="{{request.csp_nonce}}">
		var hello="world";
	</script>

Assuming the ``CSP_INCLUDE_NONCE_IN`` list contains the ``script-src`` directive, this will result in the above script being allowed.

.. Note::

   The nonce will only be added to the CSP headers if it is used.


``Context Processor``
=====================
This library contains an optional context processor, adding ``csp.context_processors.nonce`` to your configured context processors exposes a variable called ``CSP_NONCE`` into the global template context. This is simple shorthand for ``request.csp_nonce``, but can be useful if you have many occurrences of script tags.

.. code-block:: jinja

    <script nonce="{{CSP_NONCE}}">
    	var hello="world";
    </script>


``Django Template Tag/Jinja Extension``
=======================================

.. note::

   If you're making use of ``csp.extensions.NoncedScript`` you need to have ``jinja2>=2.9.6`` installed, so please make sure to either use ``django-csp[jinja2]`` in your requirements or define it yourself.


It can be easy to forget to include the ``nonce`` property in a script tag, so there is also a ``script`` template tag available for both Django templates and Jinja environments.

This tag will output a properly nonced script every time. For the sake of syntax highlighting, you can wrap the content inside of the ``script`` tag in ``<script>`` html tags, which will be subsequently removed in the rendered output. Any valid script tag attributes can be specified and will be forwarded into the rendered html.


Django Templates
----------------

Add the CSP template tags to the TEMPLATES section of your settings file:

.. code-block:: python

	TEMPLATES = [
	    {
		"OPTIONS": {
		    'libraries':          {
			'csp': 'csp.templatetags.csp',
		    }
		},
	    }
	]

Then load the ``csp`` template tags and use ``script`` in the template:

.. code-block:: jinja

	{% load csp %}
	{% script type="application/javascript" async=False %}
		<script>
			var hello='world';
		</script>
	{% endscript %}


Jinja
-----

Add ``csp.extensions.NoncedScript`` to the TEMPLATES section of your settings file:

.. code-block:: python

          TEMPLATES = [
              {
                  'BACKEND':'django.template.backends.jinja2.Jinja2',
                  'OPTIONS': {
                      'extensions': [
                          'csp.extensions.NoncedScript',
                      ],
                  }
             }
          ]


.. code-block:: jinja

	{% script type="application/javascript" async=False %}
		<script>
			var hello='world';
		</script>
	{% endscript %}


Both templates output the following with a different nonce:

.. code-block:: html

	<script nonce='123456' type="application/javascript" async=false>var hello='world';</script>

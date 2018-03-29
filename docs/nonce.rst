==============================
Using the generated CSP nonce
==============================
When ``CSP_INCLUDE_NONCE_IN`` is configured, the nonce value is returned in the CSP header. To actually make the browser do anything with this value, you will need to include it in the attributes of the tags that you wish to mark as safe.

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


``Context Processor``
=====================
This library contains an optional context processor, adding ``csp.context_processors.nonce`` to your configured context processors exposes a variable called ``nonce`` into the global template context. This is simple shorthand for ``request.csp_nonce``, but can be useful if you have many occurences of script tags.

.. code-block:: jinja

    <script nonce="{{nonce}}">
    	var hello="world";
    </script>


``Django Template Tag/Jinja Extension``
=======================================
Since it can be easy to forget to include the ``nonce`` property in a script tag, there is also a ``script`` template tag available for both Django templates and Jinja environments.

This tag will output a properly nonced script every time. For the sake of syntax highlighting, you can wrap the content inside of the ``script`` tag in ``<script>`` html tags, which will be subsequently removed in the rendered output. Any valid script tag attributes can be specified and will be forwarded into the rendered html.

Django:

.. code-block:: jinja

	{% load csp %}
	{% script type="application/javascript" async=False %}
		<script>
			var hello='world';
		</script>
	{% endscript %}


Jinja:

(assumes ``csp.extensions.NoncedScript`` is added to the jinja extensions setting)

.. code-block:: jinja

	{% script type="application/javascript" async=False %}
		<script>
			var hello='world';
		</script>
	{% endscript %}

Will output -

.. code-block:: html

	<script nonce='123456' type="application/javascript" async=false></script>


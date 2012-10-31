.. _changing-chapter:

================
Changing the CSP
================

django-csp includes decorators to enable you to change the policy on a
per-view basis.


``@csp_exempt``
===============

To stop CSP headers from being sent at all, wrap a view with
``@csp_exempt``::

    from csp.decorators import csp_exempt

    @csp_exempt
    def myview(request):
        # ...
        return render(request, ...)

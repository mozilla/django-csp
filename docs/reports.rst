.. _reports-chapter:

=====================
CSP Violation Reports
=====================

When something on a page violates the Content-Security-Policy, and the policy defines a
``report-uri`` directive, the user agent may POST a report_. Reports are JSON blobs containing
information about how the policy was violated.

Note: django-csp no longer handles report processing itself, so you will need to stand up your own
app to receive them, or else make use of a third-party report processing service.


Throttling the number of reports
--------------------------------
To throttle the number of requests made to your ``report-uri`` endpoint, you can use
``csp.contrib.rate_limiting.RateLimitedCSPMiddleware`` instead of ``csp.middleware.CSPMiddleware``
and set the ``REPORT_PERCENTAGE`` option:

``REPORT_PERCENTAGE``
    Percentage of requests that should see the ``report-uri`` directive.  Use this to throttle the
    number of CSP violation reports made to your ``report-uri``. An **integer** between 0 and 100 (0
    = no reports at all).  Ignored if ``report-uri`` isn't set.

.. _report: http://www.w3.org/TR/CSP/#sample-violation-report

.. _reports-chapter:

=====================
CSP Violation Reports
=====================

When something on a page violates the Content-Security-Policy, and the
policy defines a ``report-uri`` directive, the user agent may POST a
report_. Reports are JSON blobs containing information about how the
policy was violated.

Note: django-csp no longer handles report processing itself, so you will
need to stand up your own app to receive them, or else make use of a
third-party report processing service.

.. _report: http://www.w3.org/TR/CSP/#sample-violation-report

.. _reports-chapter:

=====================
CSP Violation Reports
=====================

When something on a page violates the Content-Security-Policy, and the
policy defines a ``report-uri`` directive, the user agent may POST a
report_. Reports are JSON blobs containing information about how the
policy was violated.

django-csp includes a view to accept and process these reports, or you
can write your own, if you need to process them differently.

The built-in report view is largely inspired by Sentry_, with all due
credit.


How reports are processed
=========================

When a report is POSTed to django-csp, a new instance of a ``Report``
object is created which stores the details of the report. django-csp
will try to determine if it has ever seen this report before.

If the report is new, a new ``Group`` will be created and an email will
be sent to the addresses in the ``ADMINS`` list.

If the report is filed into an existing ``Group``, the report will be
stored but no new group will be created and no email will be sent.


.. _report: http://www.w3.org/TR/CSP/#sample-violation-report
.. _Sentry: http://getsentry.com/

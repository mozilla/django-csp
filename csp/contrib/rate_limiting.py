import random

from django.conf import settings

from csp.middleware import CSPMiddleware


class RateLimitedCSPMiddleware(CSPMiddleware):
    """A CSP middleware that rate-limits the number of violation reports sent
    to report-uri by excluding it from some requests."""

    def get_build_kwargs(self, request, response):
        build_kwargs = super().get_build_kwargs(request, response)
        replace = build_kwargs['replace'] or {}

        report_percentage = getattr(settings, 'CSP_REPORT_PERCENTAGE')
        include_report_uri = random.random() < report_percentage
        if not include_report_uri:
            replace['report-uri'] = None
        build_kwargs['replace'] = replace

        return build_kwargs

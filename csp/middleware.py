from django.conf import settings

from csp import build_policy


class CSPMiddleware(object):
    """
    Implements the X-Content-Security-Policy response header, which
    conforming user-agents can use to restrict the permitted sources
    of various content.

    See https://wiki.mozilla.org/Security/CSP/Specification

    """

    def process_response(self, request, response):
        if getattr(response, '_csp_exempt', False):
            return response

        header = 'X-Content-Security-Policy'
        if getattr(settings, 'CSP_REPORT_ONLY', False):
            header = 'X-Content-Security-Policy-Report-Only'

        if header in response:
            # Don't overwrite existing headers.
            return response

        if getattr(settings, 'CSP_POLICY_URI', False):
            policy = 'policy-uri ' + settings.CSP_POLICY_URI
        else:
            policy = build_policy()
        response[header] = policy
        return response

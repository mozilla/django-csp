from django.conf import settings

from csp.utils import build_policy


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

        # Check for ignored path prefix.
        for prefix in getattr(settings, 'CSP_EXCLUDE_URL_PREFIXES', []):
            if request.path_info.startswith(prefix):
                return response
        
        policy = build_policy()
        
        for header in getattr(settings, 'CSP_HEADERS', set(('X-Content-Security-Policy',))):
            
            if getattr(settings, 'CSP_REPORT_ONLY', False):
                header = header + '-Report-Only'
            
            response[header] = response.get(header, policy)

        return response

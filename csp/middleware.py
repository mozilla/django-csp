from django.conf import settings
from django.utils.cache import patch_vary_headers

from csp.utils import build_policy


class CSPMiddleware(object):
    """
    Implements the Content-Security-Policy response header, which
    conforming user-agents can use to restrict the permitted sources
    of various content.

    See https://wiki.mozilla.org/Security/CSP/Specification

    """

    def process_response(self, request, response):
        if getattr(response, '_csp_exempt', False):
            return response

        # Check for ignored path prefix.
        prefixes = getattr(settings, 'CSP_EXCLUDE_URL_PREFIXES', ('/admin',))
        if request.path_info.startswith(prefixes):
            return response

        ua = request.META.get('HTTP_USER_AGENT', '')
        webkit = 'webkit' in ua.lower()
        header = 'X-WebKit-CSP' if webkit else 'Content-Security-Policy'
        if getattr(settings, 'CSP_REPORT_ONLY', False):
            header += '-Report-Only'

        patch_vary_headers(response, ['User-Agent'])
        if header in response:
            # Don't overwrite existing headers.
            return response

        response[header] = build_policy()
        return response

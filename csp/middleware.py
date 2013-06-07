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
        prefixes = getattr(settings, 'CSP_EXCLUDE_URL_PREFIXES', ('/admin',))
        if request.path_info.startswith(prefixes):
            return response

        header = 'Content-Security-Policy'
        if getattr(settings, 'CSP_REPORT_ONLY', False):
            header += '-Report-Only'

        if header in response:
            # Don't overwrite existing headers.
            return response

        config = getattr(response, '_csp_config', None)
        update = getattr(response, '_csp_update', None)
        replace = getattr(response, '_csp_replace', None)
        response[header] = build_policy(config=config, update=update,
                                        replace=replace)
        return response

from __future__ import absolute_import

from functools import partial

from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.functional import SimpleLazyObject
from django.utils.six.moves import http_client

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    class MiddlewareMixin(object):
        """
        If this middleware doesn't exist, this is an older version of django
        and we don't need it.
        """
        pass

from csp.utils import build_policy


class CSPMiddleware(MiddlewareMixin):
    """
    Implements the Content-Security-Policy response header, which
    conforming user-agents can use to restrict the permitted sources
    of various content.

    See http://www.w3.org/TR/CSP/

    """
    def _make_nonce(self, request, length=16):
        # Ensure that any subsequent calls to request.csp_nonce return the
        # same value
        if not getattr(request, '_csp_nonce', None):
            request._csp_nonce = get_random_string(length)
        return request._csp_nonce

    def process_request(self, request):
        nonce = partial(self._make_nonce, request)
        request.csp_nonce = SimpleLazyObject(nonce)

    def process_response(self, request, response):
        if getattr(response, '_csp_exempt', False):
            return response

        # Check for ignored path prefix.
        prefixes = getattr(settings, 'CSP_EXCLUDE_URL_PREFIXES', ())
        if request.path_info.startswith(prefixes):
            return response

        # Check for debug view
        status_code = response.status_code
        if status_code == http_client.INTERNAL_SERVER_ERROR and settings.DEBUG:
            return response

        header = 'Content-Security-Policy'
        if getattr(settings, 'CSP_REPORT_ONLY', False):
            header += '-Report-Only'

        if header in response:
            # Don't overwrite existing headers.
            return response

        response[header] = self.build_policy(request, response)

        return response

    def build_policy(self, request, response):
        config = getattr(response, '_csp_config', None)
        update = getattr(response, '_csp_update', None)
        replace = getattr(response, '_csp_replace', None)
        nonce = getattr(request, '_csp_nonce', None)
        return build_policy(config=config, update=update, replace=replace,
                            nonce=nonce)

from __future__ import absolute_import

import os
import base64
from collections import defaultdict
from functools import partial

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from .utils import (
    build_policy, EXEMPTED_DEBUG_CODES, HTTP_HEADERS,
)


class CSPMiddleware(MiddlewareMixin):
    """
    Implements the Content-Security-Policy response header, which
    conforming user-agents can use to restrict the permitted sources
    of various content.

    See http://www.w3.org/TR/CSP/

    """
    def _make_nonce(self, request):
        # Ensure that any subsequent calls to request.csp_nonce return the
        # same value
        if not getattr(request, '_csp_nonce', None):
            request._csp_nonce = (
                base64
                .b64encode(os.urandom(16))
                .decode("ascii")
            )
        return request._csp_nonce

    def process_request(self, request):
        nonce = partial(self._make_nonce, request)
        request.csp_nonce = SimpleLazyObject(nonce)

    def process_response(self, request, response):
        if getattr(response, '_csp_exempt', False):
            return response

        # Check for debug view
        if response.status_code in EXEMPTED_DEBUG_CODES and settings.DEBUG:
            return response

        existing_headers = {
            header for header in HTTP_HEADERS if header in response
        }
        if len(existing_headers) == len(HTTP_HEADERS):
            # Don't overwrite existing headers.
            return response

        headers = defaultdict(list)
        path_info = request.path_info

        for csp, report_only, exclude_prefixes in self.build_policy(
            request, response,
        ):
            # Check for ignored path prefix.
            for prefix in exclude_prefixes:
                if path_info.startswith(prefix):
                    break
            else:
                header = HTTP_HEADERS[int(report_only)]
                if header in existing_headers:  # don't overwrite
                    continue
                headers[header].append(csp)

        for header, policies in headers.items():
            response[header] = '; '.join(policies)
        return response

    def build_policy(self, request, response):
        build_kwargs = {
            key: getattr(response, '_csp_%s' % key, None)
            for key in ('config', 'update', 'replace', 'select')
        }
        return build_policy(
            nonce=getattr(request, '_csp_nonce', None),
            **build_kwargs,
        )

from __future__ import annotations

import base64
import http.client as http_client
import os
from functools import partial
from typing import TYPE_CHECKING

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from csp.constants import HEADER, HEADER_REPORT_ONLY
from csp.utils import build_policy

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponseBase


class CSPMiddleware(MiddlewareMixin):
    """
    Implements the Content-Security-Policy response header, which
    conforming user-agents can use to restrict the permitted sources
    of various content.

    See http://www.w3.org/TR/CSP/

    """

    def _make_nonce(self, request: HttpRequest) -> str:
        # Ensure that any subsequent calls to request.csp_nonce return the same value
        stored_nonce = getattr(request, "_csp_nonce", None)
        if isinstance(stored_nonce, str):
            return stored_nonce
        nonce = base64.b64encode(os.urandom(16)).decode("ascii")
        setattr(request, "_csp_nonce", nonce)
        return nonce

    def process_request(self, request: HttpRequest) -> None:
        nonce = partial(self._make_nonce, request)
        setattr(request, "csp_nonce", SimpleLazyObject(nonce))

    def process_response(self, request: HttpRequest, response: HttpResponseBase) -> HttpResponseBase:
        # Check for debug view
        exempted_debug_codes = (
            http_client.INTERNAL_SERVER_ERROR,
            http_client.NOT_FOUND,
        )
        if response.status_code in exempted_debug_codes and settings.DEBUG:
            return response

        csp = self.build_policy(request, response)
        if csp:
            # Only set header if not already set and not an excluded prefix and not exempted.
            is_not_exempt = getattr(response, "_csp_exempt", False) is False
            no_header = HEADER not in response
            policy = getattr(settings, "CONTENT_SECURITY_POLICY", None) or {}
            prefixes = policy.get("EXCLUDE_URL_PREFIXES", None) or ()
            is_not_excluded = not request.path_info.startswith(tuple(prefixes))
            if all((no_header, is_not_exempt, is_not_excluded)):
                response[HEADER] = csp

        csp_ro = self.build_policy_ro(request, response)
        if csp_ro:
            # Only set header if not already set and not an excluded prefix and not exempted.
            is_not_exempt = getattr(response, "_csp_exempt_ro", False) is False
            no_header = HEADER_REPORT_ONLY not in response
            policy = getattr(settings, "CONTENT_SECURITY_POLICY_REPORT_ONLY", None) or {}
            prefixes = policy.get("EXCLUDE_URL_PREFIXES", None) or ()
            is_not_excluded = not request.path_info.startswith(tuple(prefixes))
            if all((no_header, is_not_exempt, is_not_excluded)):
                response[HEADER_REPORT_ONLY] = csp_ro

        return response

    def build_policy(self, request: HttpRequest, response: HttpResponseBase) -> str:
        config = getattr(response, "_csp_config", None)
        update = getattr(response, "_csp_update", None)
        replace = getattr(response, "_csp_replace", None)
        nonce = getattr(request, "_csp_nonce", None)
        return build_policy(config=config, update=update, replace=replace, nonce=nonce)

    def build_policy_ro(self, request: HttpRequest, response: HttpResponseBase) -> str:
        config = getattr(response, "_csp_config_ro", None)
        update = getattr(response, "_csp_update_ro", None)
        replace = getattr(response, "_csp_replace_ro", None)
        nonce = getattr(request, "_csp_nonce", None)
        return build_policy(config=config, update=update, replace=replace, nonce=nonce, report_only=True)

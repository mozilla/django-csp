import random

from django.conf import settings

from csp.middleware import CSPMiddleware
from csp.utils import build_policy


class RateLimitedCSPMiddleware(CSPMiddleware):
    """A CSP middleware that rate-limits the number of violation reports sent
    to report-uri by excluding it from some requests."""

    def build_policy(self, request, response):
        config = getattr(response, "_csp_config", None)
        update = getattr(response, "_csp_update", None)
        replace = getattr(response, "_csp_replace", {})
        nonce = getattr(request, "_csp_nonce", None)

        policy = getattr(settings, "CONTENT_SECURITY_POLICY", None)

        if policy is None:
            return ""

        report_percentage = policy.get("REPORT_PERCENTAGE", 100)
        include_report_uri = random.randint(0, 100) < report_percentage
        if not include_report_uri:
            replace["report-uri"] = None

        return build_policy(config=config, update=update, replace=replace, nonce=nonce)

    def build_policy_ro(self, request, response):
        config = getattr(response, "_csp_config_ro", None)
        update = getattr(response, "_csp_update_ro", None)
        replace = getattr(response, "_csp_replace_ro", {})
        nonce = getattr(request, "_csp_nonce", None)

        policy = getattr(settings, "CONTENT_SECURITY_POLICY_REPORT_ONLY", None)

        if policy is None:
            return ""

        report_percentage = policy.get("REPORT_PERCENTAGE", 100)
        include_report_uri = random.randint(0, 100) < report_percentage
        if not include_report_uri:
            replace["report-uri"] = None

        return build_policy(config=config, update=update, replace=replace, nonce=nonce, report_only=True)

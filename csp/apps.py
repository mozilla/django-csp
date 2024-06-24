from django.apps import AppConfig
from django.core import checks

from csp.checks import check_django_csp_lt_4_0


class CspConfig(AppConfig):
    name = "csp"

    def ready(self) -> None:
        # Ignore known issue typeddjango/django-stubs #2232
        # The overload of CheckRegistry.register as a function is incomplete
        checks.register(check_django_csp_lt_4_0, checks.Tags.security)  # type: ignore

import warnings

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from . import (
    setting_to_directive,
    directive_to_setting,
    DIRECTIVES,
)


LEGACY_SETTINGS_NAMES_DEPRECATION_WARNING = (
    'The following settings are deprecated: %s. '
    'Use CSP_POLICY_DEFINITIONS and CSP_POLICIES instead.'
)


_LEGACY_SETTINGS = {
    directive_to_setting(directive) for directive in DIRECTIVES
}


def _handle_legacy_settings(csp, allow_legacy):
    """
    Custom defaults allow you to set values for csp directives
    that will apply to all CSPs defined in CSP_DEFINITIONS, avoiding
    repetition and allowing custom default values.
    """
    legacy_names = (
        _LEGACY_SETTINGS
        & set(s for s in dir(settings) if s.startswith('CSP_'))
    )
    if not legacy_names:
        return

    if not allow_legacy:
        raise ImproperlyConfigured(
            "Settings CSP_POLICY_DEFINITIONS is not allowed with following "
            "deprecated settings: %s" % ", ".join(legacy_names)
        )

    warnings.warn(
        LEGACY_SETTINGS_NAMES_DEPRECATION_WARNING % ', '.join(legacy_names),
        DeprecationWarning,
    )
    legacy_csp = (
        setting_to_directive(name, value=getattr(settings, name))
        for name in legacy_names if name not in csp
    )
    csp.update(legacy_csp)

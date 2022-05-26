import warnings

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from . import defaults


BLOCK_ALL_MIXED_CONTENT_DEPRECATION_WARNING = (
    "block-all-mixed-content is obsolete. "
    "All mixed content is now blocked if it can't be autoupgraded."
)

LEGACY_SETTINGS_NAMES_DEPRECATION_WARNING = (
    'The following settings are deprecated: %s. '
    'Use CSP_POLICY_DEFINITIONS and CSP_POLICIES instead.'
)


def setting_to_directive(setting, value, prefix='CSP_'):
    setting = setting[len(prefix):].lower()
    if setting not in defaults.PSEUDO_DIRECTIVES:
        setting = setting.replace('_', '-')
    assert setting in defaults.DIRECTIVES
    if isinstance(value, str):
        value = [value]
    return setting, value


def directive_to_setting(directive, prefix='CSP_'):
    setting = '{}{}'.format(
        prefix,
        directive.replace('-', '_').upper()
    )
    return setting


_LEGACY_SETTINGS = {
    directive_to_setting(directive) for directive in defaults.DIRECTIVES
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
            "Setting CSP_POLICY_DEFINITIONS is not allowed with the following "
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

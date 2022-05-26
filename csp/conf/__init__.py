__all__ = [
    'defaults',
    'deprecation',
    'directive_to_setting',
    'get_declared_policies',
    'get_declared_policy_definitions',
    'setting_to_directive',
    'DIRECTIVES',
]

from django.conf import settings

from . import defaults
from .deprecation import (
    directive_to_setting,
    setting_to_directive,
    _handle_legacy_settings,
)


DIRECTIVES = defaults.DIRECTIVES
PSEUDO_DIRECTIVES = defaults.PSEUDO_DIRECTIVES


def _csp_definitions_update(csp_definitions, other):
    """ Update one csp definitions dictionary with another """
    if isinstance(other, dict):
        other = other.items()
    for name, csp in other:
        csp_definitions.setdefault(name, {}).update(csp)
    return csp_definitions


def get_declared_policy_definitions():
    custom_definitions = _csp_definitions_update(
        {},
        getattr(
            settings,
            'CSP_POLICY_DEFINITIONS',
            {'default': {}},
        ),
    )
    _handle_legacy_settings(
        custom_definitions['default'],
        allow_legacy=not hasattr(settings, 'CSP_POLICY_DEFINITIONS'),
    )
    definitions = _csp_definitions_update(
        {},
        {name: defaults.POLICY for name in custom_definitions}
    )
    for name, csp in custom_definitions.items():
        definitions.setdefault(name, {}).update(csp)
    return definitions


def get_declared_policies():
    return getattr(settings, 'CSP_POLICIES', defaults.POLICIES)

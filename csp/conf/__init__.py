from . import defaults


DIRECTIVES = set(defaults.POLICY)
PSEUDO_DIRECTIVES = {d for d in DIRECTIVES if '_' in d}


def setting_to_directive(setting, value, prefix='CSP_'):
    setting = setting[len(prefix):].lower()
    if setting not in PSEUDO_DIRECTIVES:
        setting = setting.replace('_', '-')
    assert setting in DIRECTIVES
    if isinstance(value, str):
        value = [value]
    return setting, value


def directive_to_setting(directive, prefix='CSP_'):
    setting = '{}{}'.format(
        prefix,
        directive.replace('-', '_').upper()
    )
    return setting


LEGACY_KWARGS = {directive_to_setting(d, prefix='') for d in DIRECTIVES}

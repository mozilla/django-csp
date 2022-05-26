import copy
import re
import warnings

from collections import OrderedDict
from itertools import chain

from django.utils.crypto import get_random_string
from django.utils.encoding import force_str

import http.client as http_client

from .conf import (
    defaults,
    deprecation,
    setting_to_directive,
    LEGACY_KWARGS,
)


HTTP_HEADERS = (
    'Content-Security-Policy',
    'Content-Security-Policy-Report-Only',
)


EXEMPTED_DEBUG_CODES = {
    http_client.INTERNAL_SERVER_ERROR,
    http_client.NOT_FOUND,
}


def get_declared_policy_definitions():
    custom_definitions = csp_definitions_update(
        {},
        getattr(
            settings,
            'CSP_POLICY_DEFINITIONS',
            {'default': {}},
        ),
    )
    deprecation._handle_legacy_settings(
        custom_definitions['default'],
        allow_legacy=not hasattr(settings, 'CSP_POLICY_DEFINITIONS'),
    )
    definitions = csp_definitions_update(
        {},
        {name: defaults.POLICY for name in custom_definitions}
    )
    for name, csp in custom_definitions.items():
        definitions.setdefault(name, {}).update(csp)
    return definitions


def get_declared_policies():
    return getattr(settings, 'CSP_POLICIES', defaults.POLICIES)


def _normalize_config(config, key='default'):
    """
    Permits the config to be a single policy, which will be returned under the
    'default' key by default.
    """
    if config is None:
        return {}
    if not config:
        return config

    if not isinstance(next(iter(config.values())), dict):
        return {'default': config}
    return config


def build_policy(
    config=None,
    update=None,
    replace=None,
    nonce=None,
    select=None,
):
    """
    Builds the policy from the settings as a list of tuples:
    (policy_string<str>, report_only<bool>)
    """

    base_config = get_declared_policy_definitions()
    if config:
        config = _normalize_config(config)
        base_config.update(config)
        if not select:
            select = config.keys()
    replace = _normalize_config(replace) or {}
    update = _normalize_config(update) or {}
    config = {}
    for name, policy in base_config.items():
        policy = _replace_policy(policy, replace.get(name, {}))
        if update:
            update_policy = update.get(name)
            if update_policy is not None:
                _update_policy(policy, update_policy)
        config[name] = policy

    if not select:  # empty select not permitted: use csp_exempt instead
        select = get_declared_policies()
    policies = (config[name] for name in select)

    return [_compile_policy(csp, nonce=nonce) for csp in policies]


def _update_policy(csp, update):
    for k, v in update.items():
        if v is not None:
            if not isinstance(v, (list, tuple)):
                v = (v,)

            if csp.get(k) is None:
                csp[k] = v
            else:
                csp[k] += tuple(v)


def _replace_policy(csp, replace):
    new_policy = {}
    for k in set(chain(csp, replace)):
        if k in replace:
            v = replace[k]
        else:
            v = csp[k]
        if v is not None:
            v = copy.copy(v)
            if not isinstance(v, (list, tuple)):
                v = (v,)
            new_policy[k] = v
    return new_policy


def _compile_policy(csp, nonce=None):
    """
    Compile a content security policy, returning a 3-tuple:
    header_value, report_only, exclude_url_prefixes
    """
    report_uri = csp.pop(
        'report-uri',
        defaults.POLICY['report-uri'],
    )
    report_only = csp.pop(
        'report_only',
        # every directive is normalized to a tuple/list at this point
        (defaults.POLICY['report_only'],),
    )[0]
    include_nonce_in = csp.pop(
        'include_nonce_in',
        defaults.POLICY['include_nonce_in']
    )
    exclude_url_prefixes = csp.pop(
        'exclude_url_prefixes',
        defaults.POLICY['exclude_url_prefixes'],
    )

    policy_parts = {}
    for key, value in csp.items():
        # flag directives with an empty directive value
        if len(value) and value[0] is True:
            policy_parts[key] = ''
        elif len(value) and value[0] is False:
            pass
        else:  # directives with many values like src lists
            policy_parts[key] = ' '.join(value)

        if key == 'block-all-mixed-content':
            warnings.warn(
                deprecation.BLOCK_ALL_MIXED_CONTENT_DEPRECATION_WARNING,
                DeprecationWarning,
            )

    if report_uri:
        report_uri = map(force_str, report_uri)
        policy_parts['report-uri'] = ' '.join(report_uri)

    if nonce:
        for section in include_nonce_in:
            policy = policy_parts.get(section, '')
            policy_parts[section] = ("%s %s" %
                                     (policy, "'nonce-%s'" % nonce)).strip()

    policy_string = '; '.join(
        '{} {}'.format(k, val).strip() for k, val in policy_parts.items()
    )

    return policy_string, report_only, exclude_url_prefixes


def kwarg_to_directive(kwarg, value=None):
    return setting_to_directive(kwarg, prefix='', value=value)


def csp_definitions_update(csp_definitions, other):
    """ Update one csp definitions dictionary with another """
    if isinstance(other, dict):
        other = other.items()
    for name, csp in other:
        csp_definitions.setdefault(name, {}).update(csp)
    return csp_definitions


class PolicyNames:
    length = 20
    last_policy_name = None

    def __next__(self):
        self.last_policy_name = get_random_string(self.length)
        return self.last_policy_name

    def __iter__(self):
        return self


policy_names = PolicyNames()


def _clean_input_policy(policy):
    return dict(
        kwarg_to_directive(in_directive, value=value)
        if in_directive.isupper() else (in_directive, value)
        for in_directive, value in policy.items()
    )


def iter_policies(policies, name_generator=policy_names):
    """
    Accepts the following formats:
    - a policy dictionary (formatted like in settings.CSP_POLICY_DEFINITIONS)
    - an iterable of policies: (item, item, item,...)

    item can be any of the following:
        - subscriptable two-tuple: (name, csp)
        - csp dictionary which will be assigned a random name

    Yields a tuple: (name, csp)
    """
    if isinstance(policies, dict):
        yield from (
            (name, _clean_input_policy(policy))
            for name, policy in policies.items()
        )
        return

    for policy in policies:
        if isinstance(policy, (list, tuple)):
            yield (policy[0], _clean_input_policy(policy[1]))
        else:  # dictionary containing a single csp
            yield (next(name_generator), _clean_input_policy(policy))


def _kwargs_are_directives(kwargs):
    keys = set(kwargs)
    if keys.intersection(LEGACY_KWARGS):  # Legacy settings
        # Single-policy kwargs is the legacy behaviour (deprecate?)
        if keys.difference(LEGACY_KWARGS):
            raise ValueError(
                "If legacy settings are passed to the csp decorator, all "
                "kwargs must be legacy settings."
            )
        return False
    # else: a dictionary of named policies
    return True


def _policies_from_names_and_kwargs(csp_names, kwargs):
    """
    Helper used in csp_update and csp_replace to process args
    """
    if kwargs:
        if not _kwargs_are_directives(kwargs):
            policy = _clean_input_policy(kwargs)
            return {name: policy for name in csp_names}
        return dict(iter_policies(kwargs))
    else:
        raise ValueError("kwargs must not be empty.")


def _policies_from_args_and_kwargs(args, kwargs):
    all_definitions = []
    if args:  # A list of policy dictionaries
        all_definitions.append(iter_policies(args))

    if kwargs:
        if not _kwargs_are_directives(kwargs):
            kwargs = [kwargs]
        all_definitions.append(iter_policies(kwargs))

    return dict(chain(*all_definitions))


def _default_attr_mapper(attr_name, val):
    if val:
        return ' {}="{}"'.format(attr_name, val)
    else:
        return ''


def _bool_attr_mapper(attr_name, val):
    # Only return the bare word if the value is truthy
    # ie - defer=False should actually return an empty string
    if val:
        return ' {}'.format(attr_name)
    else:
        return ''


def _async_attr_mapper(attr_name, val):
    """The `async` attribute works slightly different than the other bool
    attributes. It can be set explicitly to `false` with no surrounding quotes
    according to the spec."""
    if val in [False, 'False']:
        return ' {}=false'.format(attr_name)
    elif val:
        return ' {}'.format(attr_name)
    else:
        return ''


# Allow per-attribute customization of returned string template
SCRIPT_ATTRS = OrderedDict()
SCRIPT_ATTRS['nonce'] = _default_attr_mapper
SCRIPT_ATTRS['id'] = _default_attr_mapper
SCRIPT_ATTRS['src'] = _default_attr_mapper
SCRIPT_ATTRS['type'] = _default_attr_mapper
SCRIPT_ATTRS['async'] = _async_attr_mapper
SCRIPT_ATTRS['defer'] = _bool_attr_mapper
SCRIPT_ATTRS['integrity'] = _default_attr_mapper
SCRIPT_ATTRS['nomodule'] = _bool_attr_mapper

# Generates an interpolatable string of valid attrs eg - '{nonce}{id}...'
ATTR_FORMAT_STR = ''.join(['{{{}}}'.format(a) for a in SCRIPT_ATTRS])


_script_tag_contents_re = re.compile(
    r"""<script        # match the opening script tag
            [\s|\S]*?> # minimally match attrs and spaces in opening script tag
    ([\s|\S]+)         # greedily capture the script tag contents
    </script>          # match the closing script tag
""",
    re.VERBOSE,
)


def _unwrap_script(text):
    """Extract content defined between script tags"""
    matches = re.search(_script_tag_contents_re, text)
    if matches and len(matches.groups()):
        return matches.group(1).strip()

    return text


def build_script_tag(content=None, **kwargs):
    data = {}
    # Iterate all possible script attrs instead of kwargs to make
    # interpolation as easy as possible below
    for attr_name, mapper in SCRIPT_ATTRS.items():
        data[attr_name] = mapper(attr_name, kwargs.get(attr_name))

    # Don't render block contents if the script has a 'src' attribute
    c = _unwrap_script(content) if content and not kwargs.get('src') else ''
    attrs = ATTR_FORMAT_STR.format(**data).rstrip()
    return ('<script{}>{}</script>'.format(attrs, c).strip())

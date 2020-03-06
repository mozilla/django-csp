import copy
import re

from collections import OrderedDict
from itertools import chain

from django.conf import settings
from django.utils.encoding import force_str

try:
    from django.utils.six.moves import http_client
except ImportError:
    # django 3.x removed six
    import http.client as http_client

from .conf import (
    defaults, deprecation,
    setting_to_directive, PSEUDO_DIRECTIVES,
)


HTTP_HEADERS = (
    'Content-Security-Policy',
    'Content-Security-Policy-Report-Only',
)


EXEMPTED_DEBUG_CODES = {
    http_client.INTERNAL_SERVER_ERROR,
    http_client.NOT_FOUND,
}


def from_settings():
    policies = getattr(settings, 'CSP_POLICIES', defaults.POLICIES)
    definitions = csp_definitions_update({}, defaults.POLICY_DEFINITIONS)
    custom_definitions = getattr(
        settings,
        'CSP_POLICY_DEFINITIONS',
        {'default': {}},
    )
     # Technically we're modifying Django settings here,
     # but it shouldn't matter since the end result of either will be the same
    deprecation._handle_legacy_settings(custom_definitions)
    for name, csp in custom_definitions.items():
        definitions[name].update(csp)
    # TODO: Error handling
    # TODO: Remove in October 2020 when ordered dicts are the default
    return OrderedDict(
        (name, definitions[name]) for name in policies
    )


def build_policy(config=None, update=None, replace=None, nonce=None):
    """Builds the policy as a string from the settings."""

    if config is None:
        config = from_settings()
        # Be careful, don't mutate config as it could be from settings

    update = update if update is not None else {}
    replace = replace if replace is not None else {}
    csp = {}

    for k in set(chain(config, replace)):
        if k in replace:
            v = replace[k]
        else:
            v = config[k]
        if v is not None:
            v = copy.copy(v)
            if not isinstance(v, (list, tuple)):
                v = (v,)
            csp[k] = v

    for k, v in update.items():
        if v is not None:
            if not isinstance(v, (list, tuple)):
                v = (v,)
            if csp.get(k) is None:
                csp[k] = v
            else:
                csp[k] += tuple(v)

    report_uri = csp.pop('report-uri', None)

    policy_parts = {}
    for key, value in csp.items():
        # flag directives with an empty directive value
        if len(value) and value[0] is True:
            policy_parts[key] = ''
        elif len(value) and value[0] is False:
            pass
        else:  # directives with many values like src lists
            policy_parts[key] = ' '.join(value)

    if report_uri:
        report_uri = map(force_str, report_uri)
        policy_parts['report-uri'] = ' '.join(report_uri)

    if nonce:
        include_nonce_in = getattr(settings, 'CSP_INCLUDE_NONCE_IN',
                                   ['default-src'])
        for section in include_nonce_in:
            policy = policy_parts.get(section, '')
            policy_parts[section] = ("%s %s" %
                                     (policy, "'nonce-%s'" % nonce)).strip()

    return '; '.join(['{} {}'.format(k, val).strip()
                      for k, val in policy_parts.items()])


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


def kwarg_to_directive(kwarg, value=None):
    return setting_to_directive(kwarg, prefix='', value=value)


def csp_definitions_update(csp_definitions, other):
    """ Update one csp defnitions dictionary with another """
    if isinstance(other, dict):
        other = other.items()
    for name, csp in other:
        csp_definitions.setdefault(name, {}).update(csp)
    return csp_definitions

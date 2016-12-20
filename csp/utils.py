from django.conf import settings
from django.utils.encoding import force_text
import copy
from itertools import chain
import warnings


CHILD_SRC_DEPRECATION_WARNING = \
    'child-src is deprecated in CSP v3. Use frame-src and worker-src.'


def from_settings():
    return {
        'default-src': getattr(settings, 'CSP_DEFAULT_SRC', ["'self'"]),
        'script-src': getattr(settings, 'CSP_SCRIPT_SRC', None),
        'object-src': getattr(settings, 'CSP_OBJECT_SRC', None),
        'style-src': getattr(settings, 'CSP_STYLE_SRC', None),
        'img-src': getattr(settings, 'CSP_IMG_SRC', None),
        'media-src': getattr(settings, 'CSP_MEDIA_SRC', None),
        'frame-src': getattr(settings, 'CSP_FRAME_SRC', None),
        'font-src': getattr(settings, 'CSP_FONT_SRC', None),
        'connect-src': getattr(settings, 'CSP_CONNECT_SRC', None),
        'sandbox': getattr(settings, 'CSP_SANDBOX', None),
        'report-uri': getattr(settings, 'CSP_REPORT_URI', None),
        'base-uri': getattr(settings, 'CSP_BASE_URI', None),
        'child-src': getattr(settings, 'CSP_CHILD_SRC', None),
        'form-action': getattr(settings, 'CSP_FORM_ACTION', None),
        'frame-ancestors': getattr(settings, 'CSP_FRAME_ANCESTORS', None),
        'manifest-src': getattr(settings, 'CSP_MANIFEST_SRC', None),
        'worker-src': getattr(settings, 'CSP_WORKER_SRC', None),
        'plugin-types': getattr(settings, 'CSP_PLUGIN_TYPES', None),
        'require-sri-for': getattr(settings, 'CSP_REQUIRE_SRI_FOR', None),
        'upgrade-insecure-requests': getattr(
            settings, 'CSP_UPGRADE_INSECURE_REQUESTS', False),
        'block-all-mixed-content': getattr(
            settings, 'CSP_BLOCK_ALL_MIXED_CONTENT', False),
    }


def build_policy(config=None, update=None, replace=None):
    """Builds the policy as a string from the settings."""

    if config is None:
        config = from_settings()
        # Be careful, don't mutate config as it could be from settings

    update = update if update is not None else {}
    replace = replace if replace is not None else {}
    csp = {}

    for k in set(chain(config, replace)):
        v = replace.get(k) or config[k]
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

    policy_parts = []
    for key, value in csp.items():
        # flag directives with an empty directive value
        if len(value) and value[0] is True:
            policy_parts.append(key)
        elif len(value) and value[0] is False:
            pass
        else:  # directives with many values like src lists
            policy_parts.append('%s %s' % (key, ' '.join(value)))

        if key == 'child-src':
            warnings.warn(CHILD_SRC_DEPRECATION_WARNING, DeprecationWarning)

    if report_uri:
        report_uri = map(force_text, report_uri)
        policy_parts.append('report-uri %s' % ' '.join(report_uri))

    return '; '.join(policy_parts)

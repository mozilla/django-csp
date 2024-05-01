from functools import wraps


def csp_exempt(REPORT_ONLY=None):
    if callable(REPORT_ONLY):
        raise RuntimeError(
            "Incompatible `csp_exempt` decorator usage. This decorator now requires arguments, "
            "even if none are passed. Change bare decorator usage (@csp_exempt) to parameterized "
            "decorator usage (@csp_exempt()). See the django-csp 4.0 migration guide for more "
            "information."
        )

    def decorator(f):
        @wraps(f)
        def _wrapped(*a, **kw):
            resp = f(*a, **kw)
            if REPORT_ONLY:
                resp._csp_exempt_ro = True
            else:
                resp._csp_exempt = True
            return resp

        return _wrapped

    return decorator


# Error message for deprecated decorator arguments.
DECORATOR_DEPRECATION_ERROR = (
    "Incompatible `{fname}` decorator arguments. This decorator now takes a single dict argument. "
    "See the django-csp 4.0 migration guide for more information."
)


def csp_update(config=None, REPORT_ONLY=False, **kwargs):
    if config is None and kwargs:
        raise RuntimeError(DECORATOR_DEPRECATION_ERROR.format(fname="csp_update"))

    def decorator(f):
        @wraps(f)
        def _wrapped(*a, **kw):
            resp = f(*a, **kw)
            if REPORT_ONLY:
                resp._csp_update_ro = config
            else:
                resp._csp_update = config
            return resp

        return _wrapped

    return decorator


def csp_replace(config=None, REPORT_ONLY=False, **kwargs):
    if config is None and kwargs:
        raise RuntimeError(DECORATOR_DEPRECATION_ERROR.format(fname="csp_replace"))

    def decorator(f):
        @wraps(f)
        def _wrapped(*a, **kw):
            resp = f(*a, **kw)
            if REPORT_ONLY:
                resp._csp_replace_ro = config
            else:
                resp._csp_replace = config
            return resp

        return _wrapped

    return decorator


def csp(config=None, REPORT_ONLY=False, **kwargs):
    if config is None and kwargs:
        raise RuntimeError(DECORATOR_DEPRECATION_ERROR.format(fname="csp"))

    config = {k: [v] if isinstance(v, str) else v for k, v in config.items()}

    def decorator(f):
        @wraps(f)
        def _wrapped(*a, **kw):
            resp = f(*a, **kw)
            if REPORT_ONLY:
                resp._csp_config_ro = config
            else:
                resp._csp_config = config
            return resp

        return _wrapped

    return decorator

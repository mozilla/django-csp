from functools import wraps
from itertools import chain

from .utils import (
    _policies_from_args_and_kwargs,
    _policies_from_names_and_kwargs,
)


def csp_exempt(f):
    @wraps(f)
    def _wrapped(*a, **kw):
        r = f(*a, **kw)
        r._csp_exempt = True
        return r
    return _wrapped


def csp_update(csp_names=('default',), **kwargs):
    update = _policies_from_names_and_kwargs(
        csp_names,
        kwargs,
    )

    def decorator(f):
        @wraps(f)
        def _wrapped(*a, **kw):
            r = f(*a, **kw)
            r._csp_update = update
            return r
        return _wrapped
    return decorator


def csp_replace(csp_names=('default',), **kwargs):
    replace = _policies_from_names_and_kwargs(
        csp_names,
        kwargs,
    )

    def decorator(f):
        @wraps(f)
        def _wrapped(*a, **kw):
            r = f(*a, **kw)
            r._csp_replace = replace
            return r
        return _wrapped
    return decorator


def csp(*args, **kwargs):
    config = _policies_from_args_and_kwargs(args, kwargs)

    def decorator(f):
        @wraps(f)
        def _wrapped(*a, **kw):
            r = f(*a, **kw)
            r._csp_config = config
            return r
        return _wrapped
    return decorator

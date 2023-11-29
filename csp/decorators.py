from functools import wraps
from itertools import chain

from .utils import (
    get_declared_policies,
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


def csp_select(*names):
    """
    Trim or add additional named policies.
    """
    def decorator(f):
        @wraps(f)
        def _wrapped(*a, **kw):
            r = f(*a, **kw)
            r._csp_select = names
            return r
        return _wrapped
    return decorator


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


def csp_append(*args, **kwargs):
    append = _policies_from_args_and_kwargs(args, kwargs)

    def decorator(f):
        @wraps(f)
        def _wrapped(*a, **kw):
            r = f(*a, **kw)
            # TODO: these decorators would interact more smoothly and
            # be more performant if we recorded the result on the function.
            if hasattr(r, "_csp_config"):
                r._csp_config.update({
                    name: policy for name, policy in append.items()
                    if name not in r._csp_config
                })
                select = getattr(r, "_csp_select", None)
                if select:
                    select = list(select)
                    r._csp_select = tuple(chain(
                        select,
                        (name for name in append if name not in select),
                    ))
            else:
                r._csp_config = append
                select = getattr(r, "_csp_select", None)
                if not select:
                    select = get_declared_policies()
                r._csp_select = tuple(chain(
                    select,
                    (name for name in append if name not in select),
                ))
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

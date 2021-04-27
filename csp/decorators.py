from functools import wraps

def valid_method(allowed_methods, request):
    """
        Params:
            allowed_methods:    list or string of method to make the update
            request:            the request for the csp

        Returns:
            True if the method in decorator parameter matches

        Check if any method restriction is available. If not, update is valid.
        If a list of methods is given, iterate through methods to check if request method is in restriction
        If only a method is given, check if the request method is the matching one
    """
    if allowed_methods is None:
        return True
    if isinstance(request, tuple):
        request = request[0]
    result = False
    if isinstance(allowed_methods, list):
        for method in allowed_methods:
            if request.method == method:
                result = True
                break
    elif isinstance(allowed_methods, str):
        if request.method == allowed_methods:
            result = True
    return result

def csp_exempt(methods=None, **kwargs):
    def decorator(f):
        @wraps(f)
        def _wrapped(*a, **kw):
            r = f(*a, **kw)
            if valid_method(methods, a):
                r._csp_exempt = True
            return r
        return _wrapped
    return decorator

def csp_update(methods=None, **kwargs):
    update = dict((k.lower().replace('_', '-'), v) for k, v in kwargs.items())

    def decorator(f):
        @wraps(f)
        def _wrapped(*a, **kw):
            r = f(*a, **kw)
            if valid_method(methods, a):
                r._csp_update = update
            return r
        return _wrapped
    return decorator


def csp_replace(methods=None, **kwargs):
    replace = dict((k.lower().replace('_', '-'), v) for k, v in kwargs.items())

    def decorator(f):
        @wraps(f)
        def _wrapped(*a, **kw):
            r = f(*a, **kw)
            if valid_method(methods, a):
                r._csp_replace = replace
            return r
        return _wrapped
    return decorator


def csp(methods=None, **kwargs):
    config = dict(
        (k.lower().replace('_', '-'), [v] if isinstance(v, str) else v)
        for k, v
        in kwargs.items()
    )

    def decorator(f):
        @wraps(f)
        def _wrapped(*a, **kw):
            r = f(*a, **kw)
            if valid_method(methods, a):
                r._csp_config = config
            return r
        return _wrapped
    return decorator

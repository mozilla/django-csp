from django.http import HttpResponse
from django.test import RequestFactory
from django.test.utils import override_settings

from nose.tools import eq_

from csp.middleware import CSPMiddleware
from csp.utils import build_policy


def test_empty_policy():
    policy = build_policy()
    eq_("default-src 'self'", policy)


def test_webkit_header():
    """If the browser looks like WebKit, send X-WebKit-CSP."""
    request = RequestFactory().get('/')
    mw = CSPMiddleware()

    tests = (
        # Firefox 16
        ('Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) '
         'Gecko/20121011 Firefox/16.0.1',
         False),
        # IE 10
        ('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; '
         'Trident/6.0)',
         False),
        # Safari (iPad) iOS 6
        ('Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 '
         '(KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
         True),
        # Chrome 24
        ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 '
         '(KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
         True),
    )

    def _make_test(ro=False):
        def _test(ua, is_webkit):
            suffix = '-Report-Only' if ro else ''
            request.META['HTTP_USER_AGENT'] = ua
            response = HttpResponse()
            mw.process_response(request, response)
            if is_webkit:
                assert ('X-WebKit-CSP' + suffix) in response, response
            else:
                assert ('X-Content-Security-Policy' + suffix) in response, ua
            assert 'User-Agent' in response['Vary']
        return _test

    _normal = _make_test(ro=False)
    with override_settings(CSP_REPORT_ONLY=False):
        for ua, webkit in tests:
            yield _normal, ua, webkit

    _ro = _make_test(ro=True)
    _ro = override_settings(CSP_REPORT_ONLY=True)(_ro)
    for ua, webkit in tests:
        yield _ro, ua, webkit

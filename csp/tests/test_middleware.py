from django.http import HttpResponse, HttpResponseServerError
from django.test import RequestFactory
from django.test.utils import override_settings

from csp.middleware import CSPMiddleware


HEADER = 'Content-Security-Policy'
mw = CSPMiddleware()
rf = RequestFactory()


def test_add_header():
    request = rf.get('/')
    response = HttpResponse()
    mw.process_response(request, response)
    assert HEADER in response


def test_exempt():
    request = rf.get('/')
    response = HttpResponse()
    response._csp_exempt = True
    mw.process_response(request, response)
    assert HEADER not in response


@override_settings(CSP_EXCLUDE_URL_PREFIXES=('/inlines-r-us'))
def text_exclude():
    request = rf.get('/inlines-r-us/foo')
    response = HttpResponse()
    mw.process_response(request, response)
    assert HEADER not in response


@override_settings(CSP_REPORT_ONLY=True)
def test_report_only():
    request = rf.get('/')
    response = HttpResponse()
    mw.process_response(request, response)
    assert HEADER not in response
    assert HEADER + '-Report-Only' in response


def test_dont_replace():
    request = rf.get('/')
    response = HttpResponse()
    response[HEADER] = 'default-src example.com'
    mw.process_response(request, response)
    assert response[HEADER] == 'default-src example.com'


def test_use_config():
    request = rf.get('/')
    response = HttpResponse()
    response._csp_config = {'default-src': ['example.com']}
    mw.process_response(request, response)
    assert response[HEADER] == 'default-src example.com'


def test_use_update():
    request = rf.get('/')
    response = HttpResponse()
    response._csp_update = {'default-src': ['example.com']}
    mw.process_response(request, response)
    assert response[HEADER] == "default-src 'self' example.com"


@override_settings(CSP_IMG_SRC=['foo.com'])
def test_use_replace():
    request = rf.get('/')
    response = HttpResponse()
    response._csp_replace = {'img-src': ['bar.com']}
    mw.process_response(request, response)
    policy_list = sorted(response[HEADER].split('; '))
    assert policy_list == ["default-src 'self'", "img-src bar.com"]


@override_settings(DEBUG=True)
def test_debug_exempt():
    request = rf.get('/')
    response = HttpResponseServerError()
    mw.process_response(request, response)
    assert HEADER not in response

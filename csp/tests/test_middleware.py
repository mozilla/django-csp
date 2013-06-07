from django.http import HttpResponse
from django.test import RequestFactory
from django.test.utils import override_settings

from nose.tools import eq_

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


def text_exclude():
    request = rf.get('/admin/foo')
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
    eq_(response[HEADER], 'default-src example.com')

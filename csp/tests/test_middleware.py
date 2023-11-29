from django.conf import settings
from django.http import (
    HttpResponse,
    HttpResponseServerError,
    HttpResponseNotFound,
)
from django.test import RequestFactory
from django.test.utils import override_settings

import pytest

from csp.middleware import CSPMiddleware
from csp.tests.utils import override_legacy_settings, response
from csp.utils import HTTP_HEADERS

HEADER_SET = set(HTTP_HEADERS)
HEADER, REPORT_ONLY_HEADER = HTTP_HEADERS
mw = CSPMiddleware(response())
rf = RequestFactory()


def get_headers(response):
    # TODO: use response.headers for Django 3.2+
    return set(header for header, _ in response.items())


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
    assert not HEADER_SET.intersection(get_headers(response))


@override_settings(
    CSP_POLICIES=('default', 'report'),
)
def test_exclude():
    settings.CSP_POLICY_DEFINITIONS['default']['exclude_url_prefixes'] = (
        '/inlines-r-us',
    )
    request = rf.get('/inlines-r-us/foo')
    response = HttpResponse()
    mw.process_response(request, response)
    assert HEADER not in response
    assert response[REPORT_ONLY_HEADER] == "default-src 'self'"
    settings.CSP_POLICY_DEFINITIONS['default']['exclude_url_prefixes'] = ()


@override_legacy_settings(CSP_REPORT_ONLY=True)
def test_report_only():
    request = rf.get('/')
    response = HttpResponse()
    mw.process_response(request, response)
    assert HEADER not in response
    assert REPORT_ONLY_HEADER in response


def test_dont_replace():
    request = rf.get('/')
    response = HttpResponse()
    response[HEADER] = 'default-src example.com'
    mw.process_response(request, response)
    assert response[HEADER] == 'default-src example.com'
    response = HttpResponse()
    response[REPORT_ONLY_HEADER] = 'default-src example.com'
    mw.process_response(request, response)
    assert response[REPORT_ONLY_HEADER] == 'default-src example.com'


def test_dont_replace_all():
    request = rf.get('/')
    response = HttpResponse()
    response[HEADER] = 'default-src example.com'
    response[REPORT_ONLY_HEADER] = 'default-src example.com'
    mw.process_response(request, response)
    assert response[REPORT_ONLY_HEADER] == 'default-src example.com'


def test_use_config():
    request = rf.get('/')
    response = HttpResponse()
    response._csp_config = {'default': {
        'default-src': ['example.com'],
    }}
    mw.process_response(request, response)
    assert response[HEADER] == 'default-src example.com'


def test_use_complex_config():
    request = rf.get('/')
    response = HttpResponse()
    response._csp_config = {
        'default': {
            'default-src': ['example.com'],
        },
        'report': {
            'img-src': ['test.example.com'],
            'report_only': True,
        },
    }
    mw.process_response(request, response)
    assert response[HEADER] == 'default-src example.com'
    assert response[REPORT_ONLY_HEADER] == 'img-src test.example.com'


def test_use_select():
    request = rf.get('/')
    response = HttpResponse()
    response._csp_config = {
        'alt': {
            'default-src': ['example.com'],
        },
        'child': {
            'child-src': ['child.example.com'],
        },
        'report_test': {
            'img-src': ['test.example.com'],
            'report_only': True,
        },
    }
    response._csp_select = ('child', 'default', 'report_test')
    mw.process_response(request, response)
    policies = sorted(response[HEADER].split(', '))
    assert policies == ["child-src child.example.com", "default-src 'self'"]
    assert response[REPORT_ONLY_HEADER] == 'img-src test.example.com'


def test_use_select_dne():
    request = rf.get('/')
    response = HttpResponse()
    response._csp_select = ('does_not_exist',)
    with pytest.raises(KeyError):
        mw.process_response(request, response)


def test_use_update():
    request = rf.get('/')
    response = HttpResponse()
    response._csp_update = {
        'default': {
            'default-src': ['example.com'],
            # FIXME: This won't work.  Should it?
            'report_only': True,
        },
        'does_not_exist': {
            'default-src': ['dne.example.com'],
            'report_only': True,
        },
    }
    mw.process_response(request, response)
    assert response[HEADER] == "default-src 'self' example.com"
    assert REPORT_ONLY_HEADER not in response


@override_legacy_settings(CSP_IMG_SRC=['foo.com'])
def test_use_replace():
    request = rf.get('/')
    response = HttpResponse()
    response._csp_replace = {'img-src': ['bar.com']}
    mw.process_response(request, response)
    policy_list = sorted(response[HEADER].split('; '))
    assert policy_list == ["default-src 'self'", "img-src bar.com"]


@override_legacy_settings(CSP_IMG_SRC=['foo.com'])
def test_use_complex_replace():
    request = rf.get('/')
    response = HttpResponse()
    response._csp_replace = {
        'does_not_exist': {
            'img-src': ['bar.com'],
        },
        'default': {
            'child-src': ['child.example.com'],
            'default-src': ['example.com'],
            'report_only': True,
        },
    }
    mw.process_response(request, response)
    policy_list = sorted(response[REPORT_ONLY_HEADER].split('; '))
    assert policy_list == [
        "child-src child.example.com",
        "default-src example.com",
        "img-src foo.com",
    ]
    assert HEADER not in response


@override_settings(
    DEBUG=True,
    CSP_POLICIES=("default", "report"),
)
def test_debug_errors_exempt():
    request = rf.get('/')
    response = HttpResponseServerError()
    mw.process_response(request, response)
    assert not HEADER_SET.intersection(get_headers(response))


@override_settings(
    DEBUG=True,
    CSP_POLICIES=("default", "report"),
)
def test_debug_notfound_exempt():
    request = rf.get('/')
    response = HttpResponseNotFound()
    mw.process_response(request, response)
    assert not HEADER_SET.intersection(get_headers(response))


@override_settings(
    CSP_POLICIES=("default", "report"),
)
def test_nonce_created_when_accessed():
    request = rf.get('/')
    mw.process_request(request)
    nonce = str(request.csp_nonce)
    response = HttpResponse()
    mw.process_response(request, response)
    for header in HEADER_SET:
        assert nonce in response[header]


@override_settings(
    CSP_POLICIES=("default", "report"),
)
def test_no_nonce_when_not_accessed():
    request = rf.get('/')
    mw.process_request(request)
    response = HttpResponse()
    mw.process_response(request, response)
    for header in HEADER_SET:
        assert 'nonce-' not in response[header]


@override_settings(
    CSP_POLICIES=("default", "report"),
)
def test_nonce_regenerated_on_new_request():
    request1 = rf.get('/')
    request2 = rf.get('/')
    mw.process_request(request1)
    mw.process_request(request2)
    nonce1 = str(request1.csp_nonce)
    nonce2 = str(request2.csp_nonce)
    assert request1.csp_nonce != request2.csp_nonce

    response1 = HttpResponse()
    response2 = HttpResponse()
    mw.process_response(request1, response1)
    mw.process_response(request2, response2)
    for header in HEADER_SET:
        assert nonce1 not in response2[header]
        assert nonce2 not in response1[header]


@override_legacy_settings(
    CSP_INCLUDE_NONCE_IN=[],
)
def test_no_nonce_when_disabled_by_settings():
    request = rf.get('/')
    mw.process_request(request)
    nonce = str(request.csp_nonce)
    response = HttpResponse()
    mw.process_response(request, response)
    assert nonce not in response[HEADER]

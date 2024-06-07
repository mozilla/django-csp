import pytest
from django.http import HttpResponse
from django.test import RequestFactory
from django.test.utils import override_settings

from csp.constants import HEADER, HEADER_REPORT_ONLY, NONCE
from csp.decorators import csp, csp_exempt, csp_replace, csp_update
from csp.middleware import CSPMiddleware
from csp.tests.utils import response

mw = CSPMiddleware(response())


def test_csp_exempt():
    @csp_exempt()
    def view(request):
        return HttpResponse()

    response = view(RequestFactory().get("/"))
    assert response._csp_exempt is True
    assert not hasattr(response, "_csp_exempt_ro")


def test_csp_exempt_ro():
    @csp_exempt(REPORT_ONLY=True)
    def view(request):
        return HttpResponse()

    response = view(RequestFactory().get("/"))
    assert not hasattr(response, "_csp_exempt")
    assert response._csp_exempt_ro is True


@override_settings(CONTENT_SECURITY_POLICY={"DIRECTIVES": {"img-src": ["foo.com"]}})
def test_csp_update():
    request = RequestFactory().get("/")

    def view_without_decorator(request):
        return HttpResponse()

    response = view_without_decorator(request)
    mw.process_response(request, response)
    assert HEADER_REPORT_ONLY not in response.headers
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'", "img-src foo.com"]

    @csp_update({"img-src": ["bar.com", NONCE]})
    def view_with_decorator(request):
        return HttpResponse()

    response = view_with_decorator(request)
    assert response._csp_update == {"img-src": ["bar.com", NONCE]}
    mw.process_request(request)
    assert request.csp_nonce  # Here to trigger the nonce creation.
    mw.process_response(request, response)
    assert HEADER_REPORT_ONLY not in response.headers
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'", f"img-src foo.com bar.com 'nonce-{request.csp_nonce}'"]

    response = view_without_decorator(request)
    mw.process_response(request, response)
    assert HEADER_REPORT_ONLY not in response.headers
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'", "img-src foo.com"]


@override_settings(CONTENT_SECURITY_POLICY=None, CONTENT_SECURITY_POLICY_REPORT_ONLY={"DIRECTIVES": {"img-src": ["foo.com"]}})
def test_csp_update_ro():
    request = RequestFactory().get("/")

    def view_without_decorator(request):
        return HttpResponse()

    response = view_without_decorator(request)
    mw.process_response(request, response)
    assert HEADER not in response.headers
    policy_list = sorted(response[HEADER_REPORT_ONLY].split("; "))
    assert policy_list == ["default-src 'self'", "img-src foo.com"]

    @csp_update({"img-src": ["bar.com", NONCE]}, REPORT_ONLY=True)
    def view_with_decorator(request):
        return HttpResponse()

    response = view_with_decorator(request)
    assert response._csp_update_ro == {"img-src": ["bar.com", NONCE]}
    mw.process_request(request)
    assert request.csp_nonce  # Here to trigger the nonce creation.
    mw.process_response(request, response)
    assert HEADER not in response.headers
    policy_list = sorted(response[HEADER_REPORT_ONLY].split("; "))
    assert policy_list == ["default-src 'self'", f"img-src foo.com bar.com 'nonce-{request.csp_nonce}'"]

    response = view_without_decorator(request)
    mw.process_response(request, response)
    assert HEADER not in response.headers
    policy_list = sorted(response[HEADER_REPORT_ONLY].split("; "))
    assert policy_list == ["default-src 'self'", "img-src foo.com"]


@override_settings(CONTENT_SECURITY_POLICY={"DIRECTIVES": {"img-src": ["foo.com"]}})
def test_csp_replace():
    request = RequestFactory().get("/")

    def view_without_decorator(request):
        return HttpResponse()

    response = view_without_decorator(request)
    mw.process_response(request, response)
    assert HEADER_REPORT_ONLY not in response.headers
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'", "img-src foo.com"]

    @csp_replace({"img-src": ["bar.com"]})
    def view_with_decorator(request):
        return HttpResponse()

    response = view_with_decorator(request)
    assert response._csp_replace == {"img-src": ["bar.com"]}
    mw.process_response(request, response)
    assert HEADER_REPORT_ONLY not in response.headers
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'", "img-src bar.com"]

    response = view_without_decorator(request)
    mw.process_response(request, response)
    assert HEADER_REPORT_ONLY not in response.headers
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'", "img-src foo.com"]

    @csp_replace({"img-src": None})
    def view_removing_directive(request):
        return HttpResponse()

    response = view_removing_directive(request)
    mw.process_response(request, response)
    assert HEADER_REPORT_ONLY not in response.headers
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'"]


@override_settings(CONTENT_SECURITY_POLICY=None, CONTENT_SECURITY_POLICY_REPORT_ONLY={"DIRECTIVES": {"img-src": ["foo.com"]}})
def test_csp_replace_ro():
    request = RequestFactory().get("/")

    def view_without_decorator(request):
        return HttpResponse()

    response = view_without_decorator(request)
    mw.process_response(request, response)
    assert HEADER not in response.headers
    policy_list = sorted(response[HEADER_REPORT_ONLY].split("; "))
    assert policy_list == ["default-src 'self'", "img-src foo.com"]

    @csp_replace({"img-src": ["bar.com"]}, REPORT_ONLY=True)
    def view_with_decorator(request):
        return HttpResponse()

    response = view_with_decorator(request)
    assert response._csp_replace_ro == {"img-src": ["bar.com"]}
    mw.process_response(request, response)
    assert HEADER not in response.headers
    policy_list = sorted(response[HEADER_REPORT_ONLY].split("; "))
    assert policy_list == ["default-src 'self'", "img-src bar.com"]

    response = view_without_decorator(request)
    mw.process_response(request, response)
    assert HEADER not in response.headers
    policy_list = sorted(response[HEADER_REPORT_ONLY].split("; "))
    assert policy_list == ["default-src 'self'", "img-src foo.com"]

    @csp_replace({"img-src": None}, REPORT_ONLY=True)
    def view_removing_directive(request):
        return HttpResponse()

    response = view_removing_directive(request)
    mw.process_response(request, response)
    assert HEADER not in response.headers
    policy_list = sorted(response[HEADER_REPORT_ONLY].split("; "))
    assert policy_list == ["default-src 'self'"]


def test_csp():
    request = RequestFactory().get("/")

    def view_without_decorator(request):
        return HttpResponse()

    response = view_without_decorator(request)
    mw.process_response(request, response)
    assert HEADER_REPORT_ONLY not in response.headers
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'"]

    @csp({"img-src": ["foo.com"], "font-src": ["bar.com"]})
    def view_with_decorator(request):
        return HttpResponse()

    response = view_with_decorator(request)
    assert response._csp_config == {"img-src": ["foo.com"], "font-src": ["bar.com"]}
    mw.process_response(request, response)
    assert HEADER_REPORT_ONLY not in response.headers
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["font-src bar.com", "img-src foo.com"]

    response = view_without_decorator(request)
    mw.process_response(request, response)
    assert HEADER_REPORT_ONLY not in response.headers
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'"]


def test_csp_ro():
    request = RequestFactory().get("/")

    def view_without_decorator(request):
        return HttpResponse()

    response = view_without_decorator(request)
    mw.process_response(request, response)
    assert HEADER_REPORT_ONLY not in response.headers
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'"]

    @csp({"img-src": ["foo.com"], "font-src": ["bar.com"]}, REPORT_ONLY=True)
    @csp({})  # CSP with no directives effectively removes the header.
    def view_with_decorator(request):
        return HttpResponse()

    response = view_with_decorator(request)
    assert response._csp_config_ro == {"img-src": ["foo.com"], "font-src": ["bar.com"]}
    mw.process_response(request, response)
    assert HEADER not in response.headers
    policy_list = sorted(response[HEADER_REPORT_ONLY].split("; "))
    assert policy_list == ["font-src bar.com", "img-src foo.com"]

    response = view_without_decorator(request)
    mw.process_response(request, response)
    assert HEADER_REPORT_ONLY not in response.headers
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'"]


def test_csp_string_values():
    # Test backwards compatibility where values were strings
    request = RequestFactory().get("/")

    @csp({"img-src": "foo.com", "font-src": "bar.com"})
    def view_with_decorator(request):
        return HttpResponse()

    response = view_with_decorator(request)
    assert response._csp_config == {"img-src": ["foo.com"], "font-src": ["bar.com"]}
    mw.process_response(request, response)
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["font-src bar.com", "img-src foo.com"]


# Deprecation tests


def test_csp_exempt_error():
    with pytest.raises(RuntimeError) as excinfo:

        @csp_exempt
        def view(request):
            return HttpResponse()

    assert "Incompatible `csp_exempt` decorator usage" in str(excinfo.value)


def test_csp_update_error():
    with pytest.raises(RuntimeError) as excinfo:

        @csp_update(IMG_SRC="bar.com")
        def view(request):
            return HttpResponse()

    assert "Incompatible `csp_update` decorator arguments" in str(excinfo.value)


def test_csp_replace_error():
    with pytest.raises(RuntimeError) as excinfo:

        @csp_replace(IMG_SRC="bar.com")
        def view(request):
            return HttpResponse()

    assert "Incompatible `csp_replace` decorator arguments" in str(excinfo.value)


def test_csp_error():
    with pytest.raises(RuntimeError) as excinfo:

        @csp(IMG_SRC=["bar.com"])
        def view(request):
            return HttpResponse()

    assert "Incompatible `csp` decorator arguments" in str(excinfo.value)

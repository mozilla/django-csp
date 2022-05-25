from django.http import HttpResponse
from django.test import RequestFactory
from django.test.utils import override_settings

from csp.decorators import (
    csp, csp_append, csp_replace, csp_select, csp_update, csp_exempt,
)
from csp.middleware import CSPMiddleware
from csp.tests.utils import override_legacy_settings, response
from csp.utils import policy_names, HTTP_HEADERS


HEADER, REPORT_ONLY_HEADER = HTTP_HEADERS
REQUEST = RequestFactory().get('/')
mw = CSPMiddleware(response())


def test_csp_exempt():
    @csp_exempt
    def view(request):
        return HttpResponse()
    response = view(REQUEST)
    assert response._csp_exempt


@override_settings(CSP_POLICIES=("default", "report"))
def test_csp_select():
    def view_without_decorator(request):
        return HttpResponse()
    response = view_without_decorator(REQUEST)
    mw.process_response(REQUEST, response)
    assert response[HEADER] == "default-src 'self'"
    assert response[REPORT_ONLY_HEADER] == "default-src 'self'"

    @csp_select('default')
    def view_with_decorator(request):
        return HttpResponse()
    response = view_with_decorator(REQUEST)
    assert response._csp_select == ('default',)
    mw.process_response(REQUEST, response)
    assert response[HEADER] == "default-src 'self'"
    assert REPORT_ONLY_HEADER not in response

    response = view_without_decorator(REQUEST)
    mw.process_response(REQUEST, response)
    assert response[HEADER] == "default-src 'self'"
    assert response[REPORT_ONLY_HEADER] == "default-src 'self'"


@override_legacy_settings(CSP_IMG_SRC=['foo.com'])
def test_csp_update():
    def view_without_decorator(request):
        return HttpResponse()
    response = view_without_decorator(REQUEST)
    mw.process_response(REQUEST, response)
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'", "img-src foo.com"]

    @csp_update(IMG_SRC='bar.com')
    def view_with_decorator(request):
        return HttpResponse()
    response = view_with_decorator(REQUEST)
    assert dict(response._csp_update) == {'default': {'img-src': ['bar.com']}}
    mw.process_response(REQUEST, response)
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'", "img-src foo.com bar.com"]

    response = view_without_decorator(REQUEST)
    mw.process_response(REQUEST, response)
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'", "img-src foo.com"]


@override_settings(CSP_POLICIES=('default', 'report'))
def test_csp_update_multiple():
    @csp_update(
        default={'img-src': 'bar.com'},
        report={'font-src': 'foo.com'},
    )
    def view_with_decorator(request):
        return HttpResponse()
    response = view_with_decorator(REQUEST)
    assert response._csp_update == {
        'default': {'img-src': 'bar.com'},
        'report': {'font-src': 'foo.com'},
    }
    mw.process_response(REQUEST, response)
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'", "img-src bar.com"]
    policy_list = sorted(response[REPORT_ONLY_HEADER].split("; "))
    assert policy_list == ["default-src 'self'", "font-src foo.com"]


@override_legacy_settings(CSP_IMG_SRC=['foo.com'])
def test_csp_replace():
    def view_without_decorator(request):
        return HttpResponse()
    response = view_without_decorator(REQUEST)
    mw.process_response(REQUEST, response)
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'", "img-src foo.com"]

    @csp_replace(IMG_SRC='bar.com')
    def view_with_decorator(request):
        return HttpResponse()
    response = view_with_decorator(REQUEST)
    assert dict(response._csp_replace) == {'default': {'img-src': ['bar.com']}}
    mw.process_response(REQUEST, response)
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'", "img-src bar.com"]

    response = view_without_decorator(REQUEST)
    mw.process_response(REQUEST, response)
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'", "img-src foo.com"]

    @csp_replace(IMG_SRC=None)
    def view_removing_directive(request):
        return HttpResponse()
    response = view_removing_directive(REQUEST)
    mw.process_response(REQUEST, response)
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'"]


@override_settings(CSP_POLICIES=('default', 'report'))
def test_csp_replace_multiple():
    @csp_replace(
        default={'img-src': 'bar.com', 'default-src': None},
        report={'font-src': 'foo.com'},
    )
    def view_with_decorator(request):
        return HttpResponse()
    response = view_with_decorator(REQUEST)
    assert response._csp_replace == {
        'default': {'img-src': 'bar.com', 'default-src': None},
        'report': {'font-src': 'foo.com'},
    }
    mw.process_response(REQUEST, response)
    assert response[HEADER] == "img-src bar.com"
    policy_list = sorted(response[REPORT_ONLY_HEADER].split("; "))
    assert policy_list == ["default-src 'self'", "font-src foo.com"]


def test_csp():
    def view_without_decorator(request):
        return HttpResponse()
    response = view_without_decorator(REQUEST)
    mw.process_response(REQUEST, response)
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'"]

    @csp(IMG_SRC=['foo.com'], FONT_SRC=['bar.com'])
    def view_with_decorator(request):
        return HttpResponse()
    response = view_with_decorator(REQUEST)
    assert response._csp_config == {
        policy_names.last_policy_name: {
            'img-src': ['foo.com'],
            'font-src': ['bar.com'],
        }
    }
    mw.process_response(REQUEST, response)
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["font-src bar.com", "img-src foo.com"]

    response = view_without_decorator(REQUEST)
    mw.process_response(REQUEST, response)
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["default-src 'self'"]


def test_csp_with_args():
    @csp(
        {'img-src': ['foo.com']},
        {'font-src': ['bar.com'], 'report_only': True},
    )
    def view_with_decorator(request):
        return HttpResponse()
    response = view_with_decorator(REQUEST)
    assert sorted(list(d.items()) for d in response._csp_config.values()) == [
        [('font-src', ['bar.com']), ('report_only', True)],
        [('img-src', ['foo.com'])],
    ]
    mw.process_response(REQUEST, response)
    assert response[HEADER] == "img-src foo.com"
    assert response[REPORT_ONLY_HEADER] == "font-src bar.com"


def test_csp_and_csp_select():
    @csp(new_policy={'font-src': ['bar.com']})
    @csp_select('report')  # csp doesn't override csp_select
    def view_with_decorator(request):
        return HttpResponse()

    response = view_with_decorator(REQUEST)
    assert response._csp_config == {
        'new_policy': {
            'font-src': ['bar.com'],
        },
    }
    assert response._csp_select == ('report',)
    mw.process_response(REQUEST, response)
    assert response[REPORT_ONLY_HEADER] == "default-src 'self'"
    assert HEADER not in response

    view_with_decorator = csp_select('default')(view_with_decorator)
    response = view_with_decorator(REQUEST)
    assert response._csp_select == ('default',)
    mw.process_response(REQUEST, response)
    assert response[HEADER] == "default-src 'self'"
    assert REPORT_ONLY_HEADER not in response

    view_with_decorator = csp_select('new_policy')(view_with_decorator)
    response = view_with_decorator(REQUEST)
    mw.process_response(REQUEST, response)
    assert response._csp_select == ('new_policy',)
    assert response[HEADER] == "font-src bar.com"
    assert REPORT_ONLY_HEADER not in response

    view_with_decorator = csp_select('new_policy', 'default')(
        view_with_decorator,
    )
    response = view_with_decorator(REQUEST)
    mw.process_response(REQUEST, response)
    assert response._csp_select == ('new_policy', 'default')
    assert response[HEADER] == "font-src bar.com, default-src 'self'"
    assert REPORT_ONLY_HEADER not in response


def test_csp_string_values():
    # Test backwards compatibility where values were strings
    @csp(IMG_SRC='foo.com', FONT_SRC='bar.com')
    def view_with_decorator(request):
        return HttpResponse()
    response = view_with_decorator(REQUEST)
    assert dict(response._csp_config) == {
        policy_names.last_policy_name: {
            'img-src': ['foo.com'],
            'font-src': ['bar.com'],
        }
    }
    mw.process_response(REQUEST, response)
    policy_list = sorted(response[HEADER].split("; "))
    assert policy_list == ["font-src bar.com", "img-src foo.com"]


@override_settings(CSP_POLICIES=("report",))
def test_csp_append():
    def view_without_decorator(request):
        return HttpResponse()
    response = view_without_decorator(REQUEST)
    mw.process_response(REQUEST, response)
    assert response[REPORT_ONLY_HEADER] == "default-src 'self'"
    assert HEADER not in response

    @csp_append(FONT_SRC=['bar.com'])
    def view_with_decorator(request):
        return HttpResponse()
    response = view_with_decorator(REQUEST)
    assert response._csp_config == {
        policy_names.last_policy_name: {
            'font-src': ['bar.com'],
        }
    }
    assert response._csp_select == ("report", policy_names.last_policy_name)
    mw.process_response(REQUEST, response)
    assert response[HEADER] == "font-src bar.com"
    assert response[REPORT_ONLY_HEADER] == "default-src 'self'"

    response = view_without_decorator(REQUEST)
    mw.process_response(REQUEST, response)
    assert response[REPORT_ONLY_HEADER] == "default-src 'self'"
    assert HEADER not in response


def test_csp_append_with_csp():
    @csp_append(extra={'font-src': ['bar.com']})
    @csp(default={'img-src': ['foo.com'], 'report_only': True})
    def view_with_decorator(request):
        return HttpResponse()
    response = view_with_decorator(REQUEST)
    assert response._csp_config == {
        'default': {
            'img-src': ['foo.com'],
            'report_only': True,
        },
        'extra': {
            'font-src': ['bar.com'],
        }
    }
    assert not hasattr(response, "_csp_select")
    mw.process_response(REQUEST, response)
    assert response[HEADER] == "font-src bar.com"
    assert response[REPORT_ONLY_HEADER] == "img-src foo.com"


@override_settings(CSP_POLICIES=("report", "default"))
def test_csp_append_with_csp_select():
    @csp_append(extra={'font-src': ['bar.com']})
    @csp_select("report")
    def view_with_decorator(request):
        return HttpResponse()
    response = view_with_decorator(REQUEST)
    assert response._csp_config == {
        'extra': {
            'font-src': ['bar.com'],
        }
    }
    assert response._csp_select == ("report", "extra")
    mw.process_response(REQUEST, response)
    assert response[HEADER] == "font-src bar.com"
    assert response[REPORT_ONLY_HEADER] == "default-src 'self'"


@override_settings(CSP_POLICIES=("report", "default"))
def test_csp_append_with_csp_and_csp_select():
    @csp_append(extra={'font-src': ['bar.com']})
    @csp(default={'img-src': ['foo.com'], 'report_only': True})
    @csp_select("report")
    def view_with_decorator(request):
        return HttpResponse()
    response = view_with_decorator(REQUEST)
    assert response._csp_config == {
        'default': {
            'img-src': ['foo.com'],
            'report_only': True,
        },
        'extra': {
            'font-src': ['bar.com'],
        }
    }
    assert response._csp_select == ("report", "extra")
    mw.process_response(REQUEST, response)
    assert response[HEADER] == "font-src bar.com"
    assert response[REPORT_ONLY_HEADER] == "default-src 'self'"

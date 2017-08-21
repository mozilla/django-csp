from django.http import HttpResponse
from django.test import RequestFactory

from csp.middleware import CSPMiddleware
from csp.context_processors import nonce

rf = RequestFactory()
mw = CSPMiddleware()


def test_nonce_context_processor():
    request = rf.get('/')
    mw.process_request(request)
    context = nonce(request)

    response = HttpResponse()
    mw.process_response(request, response)

    assert context['CSP_NONCE'] == request.csp_nonce


def test_nonce_context_processor_with_middleware_disabled():
    request = rf.get('/')
    context = nonce(request)

    assert context['CSP_NONCE'] == ''

from django.http import HttpResponse
from django.test import RequestFactory
from django.test.utils import override_settings

from nose.tools import eq_

from csp.middleware import CSPMiddleware
from csp.utils import build_policy


def test_empty_policy():
    policy = build_policy()
    eq_("default-src 'self'", policy)

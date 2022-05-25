from contextlib import contextmanager

from django.conf import settings
from django.http import HttpResponse
from django.template import engines, Template, Context
from django.test import override_settings, RequestFactory

from csp.middleware import CSPMiddleware


@contextmanager
def override_legacy_settings(**overrides):
    with override_settings():
        del settings.CSP_POLICY_DEFINITIONS
        for key, value in overrides.items():
            setattr(settings, key, value)
        yield


def response(*args, headers=None, **kwargs):
    def get_response(req):
        response = HttpResponse(*args, **kwargs)
        if headers:
            for k, v in headers.items():
                response.headers[k] = v
        return response
    return get_response


JINJA_ENV = engines['jinja2']
mw = CSPMiddleware(response())
rf = RequestFactory()


class ScriptTestBase(object):
    def assert_template_eq(self, tpl1, tpl2):
        aaa = tpl1.replace('\n', '').replace('  ', '')
        bbb = tpl2.replace('\n', '').replace('  ', '')
        assert aaa == bbb, "{} != {}".format(aaa, bbb)

    def process_templates(self, tpl, expected):
        request = rf.get('/')
        mw.process_request(request)
        ctx = self.make_context(request)
        return (self.make_template(tpl).render(ctx).strip(),
                expected.format(request.csp_nonce))


class ScriptTagTestBase(ScriptTestBase):
    def make_context(self, request):
        return Context({'request': request})

    def make_template(self, tpl):
        return Template(tpl)


class ScriptExtensionTestBase(ScriptTestBase):
    def make_context(self, request):
        return {'request': request}

    def make_template(self, tpl):
        return JINJA_ENV.from_string(tpl)

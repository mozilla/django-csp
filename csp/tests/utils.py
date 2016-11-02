from django.template import engines, Template, Context
from django.test import RequestFactory

from csp.middleware import CSPMiddleware


JINJA_ENV = engines['jinja2']
mw = CSPMiddleware()
rf = RequestFactory()


class ScriptTestBase(object):
    def assert_template_eq(self, tpl1, tpl2):
        aaa = tpl1.replace('\n', '').replace('  ', '')
        bbb = tpl2.replace('\n', '').replace('  ', '')
        assert aaa == bbb

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

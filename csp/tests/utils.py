from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Optional, TYPE_CHECKING, Callable, Any, Tuple, Union

from django.http import HttpResponse
from django.template import Context, Template, engines
from django.test import RequestFactory
from django.utils.functional import SimpleLazyObject

from csp.middleware import CSPMiddleware

if TYPE_CHECKING:
    from django.http import HttpRequest
    from django.template.backends.base import _EngineTemplate


def response(*args: Any, headers: Optional[Dict[str, str]] = None, **kwargs: Any) -> Callable[[HttpRequest], HttpResponse]:
    def get_response(req: HttpRequest) -> HttpResponse:
        response = HttpResponse(*args, **kwargs)
        if headers:
            for k, v in headers.items():
                response.headers[k] = v
        return response

    return get_response


JINJA_ENV = engines["jinja2"]
mw = CSPMiddleware(response())
rf = RequestFactory()


class ScriptTestBase(ABC):
    def assert_template_eq(self, tpl1: str, tpl2: str) -> None:
        aaa = tpl1.replace("\n", "").replace("  ", "")
        bbb = tpl2.replace("\n", "").replace("  ", "")
        assert aaa == bbb, f"{aaa} != {bbb}"

    def process_templates(self, tpl: str, expected: str) -> Tuple[str, str]:
        request = rf.get("/")
        mw.process_request(request)
        nonce = getattr(request, "csp_nonce")
        assert isinstance(nonce, SimpleLazyObject)
        ctx = self.make_context(request)
        return (
            self.make_template(tpl).render(ctx).strip(),  # type: ignore
            expected.format(nonce),
        )

    @abstractmethod
    def make_context(self, request: HttpRequest) -> Union[dict[str, Any], Context]: ...

    @abstractmethod
    def make_template(self, tpl: str) -> Union[_EngineTemplate, Template]: ...


class ScriptTagTestBase(ScriptTestBase):
    def make_context(self, request: HttpRequest) -> Context:
        return Context({"request": request})

    def make_template(self, tpl: str) -> Template:
        return Template(tpl)


class ScriptExtensionTestBase(ScriptTestBase):
    def make_context(self, request: HttpRequest) -> dict[str, HttpRequest]:
        return {"request": request}

    def make_template(self, tpl: str) -> _EngineTemplate:
        return JINJA_ENV.from_string(tpl)

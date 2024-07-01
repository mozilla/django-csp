from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Literal

if TYPE_CHECKING:
    from django.http import HttpRequest


def nonce(request: HttpRequest) -> Dict[Literal["CSP_NONCE"], str]:
    nonce = request.csp_nonce if hasattr(request, "csp_nonce") else ""

    return {"CSP_NONCE": nonce}

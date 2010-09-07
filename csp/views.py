import json

from django.conf import settings
from django.core.mail import mail_admins
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader, Context
from django.views.decorators.http import require_POST


@require_POST
def report(request):
    """
    Accept a Content Security Policy violation report and forward
    the report via email to CSP_NOTIFY (defaults to ADMINS).

    """
    try:
        violation = json.loads(request.raw_post_data)
    except Exception:
        return HttpResponseBadRequest()

    c = Context(violation)
    t = loader.get_template('csp/email/report.ltxt')
    body = t.render(c)

    mail_admins('CSP Violation', body)
    return HttpResponse()

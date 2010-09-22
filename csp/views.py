import json

from django.core.mail import mail_admins
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader, Context
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from csp import build_policy


@csrf_exempt
@require_POST
def report(request):
    """
    Accept a Content Security Policy violation report and forward
    the report via email to ADMINS.

    """

    try:
        violation = json.loads(request.raw_post_data)['csp-report']
    except Exception:
        return HttpResponseBadRequest()

    data = {}
    for key in violation:
        data[key.replace('-', '_')] = violation[key]

    c = Context(data)
    t = loader.get_template('csp/email/report.ltxt')
    body = t.render(c)

    subject = 'CSP Violation: %s: %s' % (data['blocked_uri'],
                                         data['violated_directive'])
    mail_admins(subject, body)
    return HttpResponse()


def policy(request):
    """
    Returns a valid policy-uri, as an alternative to putting the whole
    policy in the header.

    """

    policy = build_policy()

    return HttpResponse(policy, mimetype='text/x-content-security-policy')

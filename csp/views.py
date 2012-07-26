from django.contrib.sites.models import RequestSite
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from csp.utils import build_policy
from csp.models import Report


@csrf_exempt
@require_POST
def report(request):
    """
    Accept a Content Security Policy violation report and store it.

    We store a CSP report in the database. If the report looks new, according
    to a heuristic, a new Report Group will be created and admins, or the
    addresses defined in :ref:`CSP_NOTIFY`, will be notified.

    """

    violation = request.raw_post_data
    Report.create(violation).save(RequestSite(request))

    return HttpResponse()

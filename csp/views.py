import json

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template import loader, Context


def report(request):
    """
    Accept a Content Security Policy violation report and forward
    the report via email to CSP_NOTIFY (defaults to ADMINS).

    """
    return HttpResponse()

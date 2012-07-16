from django.core.mail import send_mail, mail_admins
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import loader, Context


def build_policy():
    """Builds the policy as a string from the settings."""

    policy = ['default-src %s' % (' '.join(settings.CSP_DEFAULT_SRC) if
                            hasattr(settings, 'CSP_DEFAULT_SRC') else
                            "'self'")]
    if hasattr(settings, 'CSP_IMG_SRC'):
        policy.append('img-src %s' % ' '.join(settings.CSP_IMG_SRC))
    if hasattr(settings, 'CSP_SCRIPT_SRC'):
        policy.append('script-src %s' % ' '.join(settings.CSP_SCRIPT_SRC))
    if hasattr(settings, 'CSP_OBJECT_SRC'):
        policy.append('object-src %s' % ' '.join(settings.CSP_OBJECT_SRC))
    if hasattr(settings, 'CSP_MEDIA_SRC'):
        policy.append('media-src %s' % ' '.join(settings.CSP_MEDIA_SRC))
    if hasattr(settings, 'CSP_FRAME_SRC'):
        policy.append('frame-src %s' % ' '.join(settings.CSP_FRAME_SRC))
    if hasattr(settings, 'CSP_FONT_SRC'):
        policy.append('font-src %s' % ' '.join(settings.CSP_FONT_SRC))
    if hasattr(settings, 'CSP_CONNECT_SRC'):
        policy.append('connect-src %s' % ' '.join(settings.CSP_CONNECT_SRC))
    if hasattr(settings, 'CSP_STYLE_SRC'):
        policy.append('style-src %s' % ' '.join(settings.CSP_STYLE_SRC))
    if hasattr(settings, 'CSP_SANDBOX'):
        policy.append('sandbox %s' % ' '.join(settings.CSP_SANDBOX))
    if hasattr(settings, 'CSP_REPORT_URI'):
        policy.append('report-uri %s' % settings.CSP_REPORT_URI)

    return '; '.join(policy)


def send_new_mail(sender, report, site=None, **kw):
    subject = 'New CSP Violation: %s' % sender.name
    url = reverse('admin:csp_report_change', args=(report.id,))
    if site is not None:
        url = ''.join(('http://', site.domain, url))
    data = report.__dict__
    data.update({'name': sender.name,
                 'identifier': sender.identifier,
                 'url': url})
    c = Context(data)
    t = loader.get_template('csp/email/new_report.ltxt')
    body = t.render(c)

    if hasattr(settings, 'CSP_NOTIFY'):
        send_mail(subject, body, settings.SERVER_EMAIL, settings.CSP_NOTIFY)
    else:
        mail_admins(subject, body)

from django.conf import settings


class CSPMiddleware(object):
    """
    Implements the X-Content-Security-Policy response header, which
    conforming user-agents can use to restrict the permitted sources
    of various content.

    See https://wiki.mozilla.org/Security/CSP/Specification

    """

    def process_response(self, request, response):
        if 'x-content-security-policy' in response:
            # Don't overwrite existing headers.
            return response

        policy = ['allow %s' % (' '.join(settings.CSP_ALLOW) if
                                hasattr(settings, 'CSP_ALLOW') else
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
        if hasattr(settings, 'CSP_XHR_SRC'):
            policy.append('xhr-src %s' % ' '.join(settings.CSP_XHR_SRC))
        if hasattr(settings, 'CSP_STYLE_SRC'):
            policy.append('style-src %s' % ' '.join(settings.CSP_STYLE_SRC))
        if hasattr(settings, 'CSP_FRAME_ANCESTORS'):
            policy.append('frame-ancestors %s' %
                          ' '.join(settings.CSP_FRAME_ANCESTORS))
        if hasattr(settings, 'CSP_REPORT_URI'):
            policy.append('report-uri %s' % settings.CSP_REPORT_URI)
        if hasattr(settings, 'CSP_POLICY_URI'):
            policy.append('policy-uri %s' % settings.CSP_POLICY_URI)

        response['X-Content-Security-Policy'] = '; '.join(policy)
        return response

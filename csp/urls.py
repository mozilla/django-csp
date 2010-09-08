from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('csp.views',
    url(r'^/report', 'report', name='csp.report'),
    url(r'^/policy', 'policy', name='csp.policy'),
)

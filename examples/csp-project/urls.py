from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.http import HttpResponseNotFound, HttpResponseServerError

from csp import views


handler404 = lambda r: HttpResponseNotFound()
handler500 = lambda r: HttpResponseServerError()

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls))
)

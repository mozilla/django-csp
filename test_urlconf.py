from django.conf.urls import patterns, url, include
from django.contrib import admin

urlpatterns = patterns("",
    url(r'django_admin/', include(admin.site.urls)),
)

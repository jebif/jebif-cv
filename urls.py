from django.conf.urls.defaults import *
from django.contrib import admin

from jebif import settings

urlpatterns = patterns('',
    (r'^cv/',           include('candidate.urls')),
    (r'^users/',        include('users.urls')),
    (r'^accounts/',     include('registration.urls')),
)
urlpatterns += patterns('django.views.generic.simple',
    # Homepage
    (r'', 'direct_to_template', {'template': 'homepage.html'}),
)


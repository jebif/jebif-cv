from django.conf.urls.defaults import *
from django.contrib import admin

from jebif_cv import settings

admin.autodiscover()

urlpatterns = patterns('',
    # add 'django.contrib.admindocs' to INSTALLED_APPS 
    # to enable admin documentation
    # (r'^admin/doc/',    include('django.contrib.admindocs.urls')),
    
    (r'^cv/',           include('candidate.urls')),
    (r'^users/',        include('users.urls')),
    (r'^admin/',        include(admin.site.urls)),
    (r'^accounts/',     include('registration.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
)

urlpatterns += patterns('django.views.generic.simple',
    # Homepage
    (r'', 'direct_to_template', {'template': 'homepage.html'}),
)
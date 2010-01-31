from django.conf.urls.defaults import *
from candidate.views import collection, entry, edit, new, toggle_valid

urlpatterns = patterns('',
    url(r'(?P<cv_id>\d+)/edit/$', 
        edit, 
        name = "cv_edit"
    ),
    url(r'(?P<cv_id>\d+)/validation/$',
        toggle_valid,
        name = "cv_toggle_valid"
    ),
    url(r'(?P<cv_id>\d+)/$', 
        entry, 
        name = "cv_entry"
    ),
    url(r'new/$', 
        new,
        name = "cv_new"
    ),
    url(r'^$', 
        collection, 
        name = "cv_collection"
    )
)
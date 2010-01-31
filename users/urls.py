from django.conf.urls.defaults import *
from users.views import collection, entry, edit, new, delete, change_password

urlpatterns = patterns('',
    url(r'(?P<user_id>\d+)/edit/$', 
        edit, 
        name = "user_edit"
    ),
    url(r'(?P<user_id>\d+)/change_password/$',
        change_password,
        name = "change_password"
    ),
    url(r'(?P<user_id>\d+)/delete/$', 
        delete, 
        name = "user_delete"
    ),
    url(r'(?P<user_id>\d+)/$', 
        entry, 
        name = "user_entry"
    ),
    url(r'new/$',
        new,
        name = "user_new"
    ),
    url(r'^$', 
        collection, 
        name = "user_collection"
    )
)
"""
URLConf for Django user registration.

Recommended usage is to use a call to ``include()`` in your project's
root URLConf to include this URLConf for any URL begninning with
'/accounts/'.

"""

from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout, logout_then_login
from django.core.urlresolvers import reverse
from django.conf import settings
from registration.views import send_password

ROOT_URL = "%scv/" % settings.ROOT_URL

urlpatterns = patterns('',
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]+ because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^login/$', login, name = "login"),
    url(r'^logout/$', logout_then_login, {'login_url' : '/%saccounts/login/?next=/%s'%(ROOT_URL, ROOT_URL)}, name="logout"),
    url(r'^send_password/$', send_password, name = "registration_send_password"),
    #(r'^activate/(?P<activation_key>\w+)/$', activate),
    #(r'^register/$', register),
    #(r'^register/complete/$', direct_to_template, {'template': 'registration/registration_complete.html'}),
)

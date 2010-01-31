# -*- encoding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context, loader
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from models import RegistrationProfile
from forms import RegistrationForm


def activate(request, activation_key):
    """
    Activates a user's account, if their key is valid and hasn't
    expired.

    Context::
        account
            The ``User`` object corresponding to the account,
            if the activation was successful.

        expiration_days
            The number of days for which activation keys stay valid.

    Template::
        registration/activate.html

    """
    activation_key = activation_key.lower() # Normalize before trying anything with it.
    account = RegistrationProfile.objects.activate_user(activation_key)
    return render_to_response('registration/activate.html',
                              {'account': account,
                               'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS },
                              context_instance=RequestContext(request))

def register(request, success_url='/accounts/register/complete/'):
    """
    Allows a new user to register an account.

    On successful registration, an email will be sent to the new user
    with an activation link to click to make the account active. This
    view will then redirect to ``success_url``, which defaults to
    '/accounts/register/complete/'. This application has a URL pattern
    for that URL and routes it to the ``direct_to_template`` generic
    view to display a short message telling the user to check their
    email for the account activation link.

    Context::
        form
            The registration form

    Template::
        registration/registration_form.html

    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = RegistrationProfile.objects.create_inactive_user(username=data['username'],
                                                                        email=data['email'])
            return HttpResponseRedirect(success_url)
    else:
        form = RegistrationForm()
    return render_to_response('registration/registration_form.html',
                              { 'form': form },
                              context_instance=RequestContext(request))

def send_password(request):
    if request.method == 'POST':
        if request.POST:
            try:
                user = User.objects.get(username=request.POST['username'])
            except User.DoesNotExist:
                return HttpResponseRedirect(reverse('accounts_login'))
            current_domain = Site.objects.get_current().domain
            subject = "[AGESUR] Modification du mot de passe"
            message_template = loader.get_template('registration/password_email.txt')
            message_context = Context(
                {
                    'user': user.username,
                    'site_url': 'http://%s/' % current_domain,
                    'activation_key': user.password
                })
            message = message_template.render(message_context)
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    return HttpResponseRedirect(reverse('accounts_login'))

def modify_password(request):
    pass

def modify_account(request):
    pass

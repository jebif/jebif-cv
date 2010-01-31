"""
Form and validation code for user registration.

"""

from django import forms
from django.contrib.auth.models import User

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary.
attrs_dict = { 'class': 'required' }

class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the password is entered twice and matches,
    and that the username is not already taken.

    """
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs=attrs_dict),
                               label=u'Username')
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, max_length=200)),
                             label=u'Email address',
                             required=False)

    def clean_username(self):
        """
        Validates that the username is not already in use.

        """
        if self.cleaned_data.get('username', None):
            try:
                user = User.objects.get(username__exact=self.cleaned_data['username'])
            except User.DoesNotExist:
                return self.cleaned_data['username']
        raise forms.ValidationError(u'L\'utilisateur "%s" existe déjà.' % self.cleaned_data['username'])



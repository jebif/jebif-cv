from django.forms import ModelForm

from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username','is_superuser','groups','first_name','last_name','email')
    

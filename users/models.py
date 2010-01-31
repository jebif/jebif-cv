from django.db import models

from django.contrib.auth.models import User

from signals import create_profile_for_user
from candidate.models import CV

# After a user (new or existing) is saved, if he has not a related profile,
# this signal will create one.
models.signals.post_save.connect(create_profile_for_user, sender = User)

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    cv = models.ForeignKey(CV, null = True, blank = True)

    def is_employer(self):
        return self.user.groups.filter(name__in = "employeur").count > 0
    
    def is_candidate(self):
        return self.user.groups.filter(name__in = "candidat").count > 0
    

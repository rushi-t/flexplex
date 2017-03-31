from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # custom fields for user
    phone = models.CharField(max_length=15)

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # custom fields for user
    phone = models.CharField(max_length=15)

    ACTIVATION_STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Activated'),
        (2, 'Deactivated'),

    )
    activation_status = models.IntegerField(choices=ACTIVATION_STATUS_CHOICES, default=ACTIVATION_STATUS_CHOICES[0][0])

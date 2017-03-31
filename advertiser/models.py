from __future__ import unicode_literals

# models.py
from django.db import models
from hoarder.models import Hoarding

class Campaign(models.Model):
    user = models.ForeignKey('auth.User')
    resource = models.FileField()
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)


class CampaignHoardings(models.Model):
    campaign = models.ForeignKey('Campaign')
    hoarding = models.ForeignKey('hoarder.Hoarding')

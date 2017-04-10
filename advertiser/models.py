from __future__ import unicode_literals

# models.py
import uuid
from django.db import models

class Campaign(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('auth.User')
    resource = models.FileField(null=True)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)


class CampaignHoardings(models.Model):
    campaign = models.ForeignKey('Campaign', related_name='hoardings', on_delete=models.CASCADE)
    hoarding = models.ForeignKey('hoarder.Hoarding')

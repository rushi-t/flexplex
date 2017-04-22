from __future__ import unicode_literals

# models.py
import uuid
from django.db import models

class Campaign(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('auth.User')
    name = models.CharField(default='', max_length=100)
    resource = models.FileField(null=True)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    CONTENT_STATUS_TYPE_CHOICES = (
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Rejected'),
    )
    content_status = models.IntegerField(choices=CONTENT_STATUS_TYPE_CHOICES, default=0)
    creation_date = models.DateTimeField(auto_now_add=True)


class CampaignHoardings(models.Model):
    campaign = models.ForeignKey('Campaign', related_name='hoardings', on_delete=models.CASCADE)
    hoarding = models.ForeignKey('hoarder.Hoarding')
    STATUS_TYPE_CHOICES = (
        (0, 'Pending'),
        (1, 'Accepted'),
        (2, 'Rejected'),
    )
    status = models.IntegerField(choices=STATUS_TYPE_CHOICES, default=0)

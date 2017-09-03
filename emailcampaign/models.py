# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    #country = models.ForeignKey('Country')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()

class Campaign(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)


class CampaignUser(models.Model):
    campaign = models.ForeignKey('Campaign')
    user = models.ForeignKey('User')
    is_read = models.BooleanField(default=False)


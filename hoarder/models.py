from __future__ import unicode_literals
import uuid
from django.db import models

# Create your models here.

class Hoarding(models.Model):
    #uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey('auth.User')
    address = models.ForeignKey('common.Address', default=None)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    DISPLAY_TYPE_CHOICES = (
        (1, 'Indoor'),
        (2, 'OutDoor'),
    )
    display_type = models.IntegerField(choices=DISPLAY_TYPE_CHOICES, default=2)

    COST_CYCLE_CHOICES = (
        (1, 'Daily'),
        (2, 'Weekly'),
        (3, 'Monthly'),
    )
    cost_cycle = models.IntegerField(choices=COST_CYCLE_CHOICES, default=3)
    cost = models.FloatField(default=0)

    creation_date = models.DateTimeField(auto_now_add=True)
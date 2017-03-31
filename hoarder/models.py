from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Hoarding(models.Model):
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

    created = models.DateTimeField(
        blank=True, null=True)
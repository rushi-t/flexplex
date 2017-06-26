from __future__ import unicode_literals
import uuid
from django.db import models
from datetime import datetime
from datetime import date
from django.db.models import Q
from advertiser.models import Campaign, CampaignHoardings
# Create your models here.

class Hoarding(models.Model):
    #uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey('auth.User')
    address = models.ForeignKey('common.Address', default=None)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    h_res = models.PositiveIntegerField(default=0)
    v_res = models.PositiveIntegerField(default=0)

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

    start_time = models.TimeField(default='00:00 AM')
    stop_time = models.TimeField(default='00:00 AM')

    cost_cycle = models.IntegerField(choices=COST_CYCLE_CHOICES, default=3)
    cost = models.FloatField(default=0)

    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(default=datetime.now())
    last_heartbeat = models.DateTimeField(default=datetime.now())

    def save(self, last_update=True, *args, **kwargs):
        if last_update is True:
            self.last_update = datetime.now()
        super(Hoarding, self).save(*args, **kwargs)

    def get_resources(self):
        resources = HoardingResource.objects.filter(hoarding=self)
        return resources

    def get_hardware_status(self):
        diff = (datetime.now() - self.last_heartbeat.replace(tzinfo=None)).total_seconds() / 60.0
        if diff > 5:
            return 0
        else:
            return 1

    def get_all_ads(self):
        today = date.today()
        campaigns = CampaignHoardings.objects.filter(hoarding=self, status=CampaignHoardings.STATUS_TYPE_CHOICES[1][0]). \
            only('campaign')
        return campaigns

    def get_running_ads(self):
        today = date.today()
        campaigns = CampaignHoardings.objects.filter(hoarding=self, status=CampaignHoardings.STATUS_TYPE_CHOICES[1][0]).\
                    only('campaign').filter(Q(campaign__from_date__lte=today) & Q(campaign__to_date__gte=today))
        return campaigns

    def get_scheduled_ads(self):
        today = date.today()
        campaigns = CampaignHoardings.objects.filter(hoarding=self, status=CampaignHoardings.STATUS_TYPE_CHOICES[1][0]).\
                    only('campaign').filter(campaign__from_date__gt=today)
        return campaigns

    def get_pending_ads(self):
        today = date.today()
        campaigns = CampaignHoardings.objects.filter(hoarding=self, status=CampaignHoardings.STATUS_TYPE_CHOICES[0][0]).\
                    only('campaign').filter(campaign__from_date__gt=today)
        return campaigns


class HoardingResource(models.Model):
    hoarding = models.ForeignKey('Hoarding', default=None)
    resource = models.FileField(null=True)
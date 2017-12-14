from __future__ import unicode_literals
import uuid
from django.db import models
from datetime import datetime
from datetime import date
from django.db.models import Q
from advertiser.models import Campaign, CampaignHoardings, CampaignImpressions
from django.db.models import Avg
import random

class Hoarding(models.Model):
    #uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey('auth.User')
    address = models.ForeignKey('common.Address', default=None)
    description = models.CharField(max_length=100, default='')

    DISPLAY_TYPE_CHOICES = ( (1, 'Indoor'), (2, 'OutDoor'), (3, 'CinemaHall'))
    display_type = models.IntegerField(choices=DISPLAY_TYPE_CHOICES, default=2)
    # For Outdoor Display
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    # For Indoor Display
    diagonal_size = models.PositiveIntegerField(default=0)

    DIMENSION_UNIT_CHOICES = ( (1, 'inch'), (2, 'feet'), )
    dimension_unit = models.IntegerField(choices=DIMENSION_UNIT_CHOICES, default=2)

    PIXEL_PITCH_CHOICES = ( (3, 'P3'), (4, 'P4'), (5, 'P5'), (6, 'P6'), (7, 'P7'), (8, 'P8'), (9, 'P9'), (10, 'P10'), (12, 'P12'), (14, 'P14'), (16, 'P16'), )
    pixel_pitch = models.IntegerField(choices=PIXEL_PITCH_CHOICES, default=0)

    h_res = models.PositiveIntegerField(default=0)
    v_res = models.PositiveIntegerField(default=0)

    # COST_CYCLE_CHOICES = ( (1, 'Daily'), (2, 'Weekly'), (3, 'Monthly'), )
    # cost_cycle = models.IntegerField(choices=COST_CYCLE_CHOICES, default=3)

    rate = models.FloatField(default=0)
    min_duration = models.PositiveIntegerField(default=15)

    start_time = models.TimeField(default='08:00 AM')
    stop_time = models.TimeField(default='12:00 PM')

    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(default=datetime.now())
    last_heartbeat = models.DateTimeField(default=datetime.now())

    active_status = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    def get_rate(self):
        return ('%f' % self.rate).rstrip('0').rstrip('.')

    def get_display_dimension(self):
        display_str = ''
        if self.display_type == self.DISPLAY_TYPE_CHOICES[1][0]:
            display_str = str(self.width) + " x " + str(self.height) \

        else:
            display_str = str(self.diagonal_size)
        display_str = display_str + " " + self.DIMENSION_UNIT_CHOICES[self.dimension_unit-1][1]
        return display_str

    def save(self, last_update=True, *args, **kwargs):
        if last_update is True:
            self.last_update = datetime.now()
        super(Hoarding, self).save(*args, **kwargs)

    def get_resources(self):
        resources = HoardingResource.objects.filter(hoarding=self)
        return resources

    def get_hardware_status(self):
        diff = abs(datetime.now() - self.last_heartbeat.replace(tzinfo=None)).total_seconds() / 60.0
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

    def get_avg_monthly_impressions(self):
        try:
            today = date.today()
            avg_impression = int(CampaignImpressions.objects.filter(hoarding=self, date__month=today.month).aggregate(Avg('impression_count')).values()[0])
            return avg_impression
        except:
            return 0

    def get_revenue(self):
        return random.randint(0,9)

def get_active_hoardings():
    return Hoarding.objects.filter(active_status=True)

class HoardingResource(models.Model):
    hoarding = models.ForeignKey('Hoarding', default=None)
    resource = models.FileField(null=True)
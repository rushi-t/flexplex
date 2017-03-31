from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # custom fields for user
    phone = models.CharField(max_length=15)

class Country(models.Model):
    name = models.CharField(max_length=20)

class State(models.Model):
    #country = models.ForeignKey('Country')
    name = models.CharField(max_length=20)

class City(models.Model):
    #state = models.ForeignKey('State')
    name = models.CharField(max_length=20)

class Address(models.Model):
    city = models.ForeignKey('City')
    state = models.ForeignKey('State')
    country = models.ForeignKey('Country')
    address = models.CharField(max_length=200)
    geo_location = models.CharField(max_length=50)
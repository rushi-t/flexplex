from common import models
from rest_framework import serializers


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = "__all__"

class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.State
        fields = "__all__"

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Country
        fields = "__all__"

class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer();
    state = StateSerializer();
    country = CountrySerializer();
    class Meta:
        model = models.Address
        # fields = "__all__"
        exclude = ('id',)
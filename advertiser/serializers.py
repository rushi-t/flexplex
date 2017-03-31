# serializers.py
from rest_framework import serializers
from advertiser.models import Campaign, CampaignHoardings
from  hoarder.serializers import HoardingSerializer

class CampaignSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(read_only=True, slug_field='id')
    class Meta:
        model = Campaign
        fields = ('resource', 'from_date', 'to_date', 'created',)

class CampaignHoardingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignHoardings
        fields = ('campaign', 'hoarding')
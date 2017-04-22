# serializers.py
from rest_framework import serializers
from advertiser.models import Campaign, CampaignHoardings
from hoarder.models import Hoarding
from hoarder.serializers import HoardingSerializer

class CampaignHoardingsSerializer(serializers.ModelSerializer):
    hoarding = HoardingSerializer()
    class Meta:
        model = CampaignHoardings
        fields = ('hoarding',)

class CampaignSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(read_only=True, slug_field='id')
    hoardings = CampaignHoardingsSerializer(many=True)
    class Meta:
        model = Campaign
        fields = ('name', 'resource', 'from_date', 'to_date', 'content_status', 'creation_date', 'hoardings')

    def create(self, validated_data):
        hoardings_data = validated_data.pop('hoardings')
        campaign = Campaign.objects.create(**validated_data)
        for hoarding_data in hoardings_data:
            hoarding = Hoarding.objects.get(id=hoarding_data['hoarding'].id)
            CampaignHoardings.objects.create(campaign=campaign, hoarding=hoarding)
        return campaign

class CampaignResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('resource',)
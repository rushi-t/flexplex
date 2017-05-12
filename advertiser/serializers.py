# serializers.py
from rest_framework import serializers
from advertiser.models import Campaign, CampaignHoardings
from hoarder.models import Hoarding
from hoarder.serializers import HoardingSerializer
from django.contrib.sites.models import Site


class CampaignSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.SlugRelatedField(read_only=True, slug_field='id')
    # hoardings = CampaignHoardingsSerializer(many=True)


    def to_representation(self, instance):
        representation = super(CampaignSerializer, self).to_representation(instance)
        request = self.context.get('request')
        domain_name = request.scheme + "://" + request.META['HTTP_HOST']
        full_path = domain_name + instance.resource.name
        representation['resource'] = full_path
        return representation

    class Meta:
        model = Campaign
        fields = ('name', 'resource', 'from_date', 'to_date', 'content_status', 'creation_date')

    def create(self, validated_data):
        hoardings_data = validated_data.pop('hoardings')
        campaign = Campaign.objects.create(**validated_data)
        for hoarding_data in hoardings_data:
            hoarding = Hoarding.objects.get(id=hoarding_data['hoarding'].id)
            CampaignHoardings.objects.create(campaign=campaign, hoarding=hoarding)
        return campaign

class CampaignHoardingsSerializer(serializers.ModelSerializer):
    hoarding = HoardingSerializer()
    campaign = CampaignSerializer()
    class Meta:
        model = CampaignHoardings
        fields = ('hoarding', 'campaign')

class CampaignResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('hoarding',)
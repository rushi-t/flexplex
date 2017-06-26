from rest_framework import serializers
from hoarder.models import Hoarding, HoardingResource
from django.contrib.auth.models import User
from common.serializers import AddressSerializer
from common.models import Address
from advertiser.serializers import CampaignHoardingsSerializer, CampaignSerializer
from advertiser.models import CampaignHoardings, Campaign
from datetime import date
from django.db.models import Q

class HoardingResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoardingResource

class HoardingSerializer(serializers.HyperlinkedModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    address = AddressSerializer()
    campaigns = serializers.SerializerMethodField()

    def get_campaigns(self, obj):
        campaign_hoarding_query = CampaignHoardings.objects.filter(hoarding=obj).\
            filter(status=CampaignHoardings.STATUS_TYPE_CHOICES[1][0]). \
            filter(Q(campaign__from_date__lte=date.today()) & Q(campaign__to_date__gte=date.today())).\
            values('campaign')
        campaign_query = Campaign.objects.filter(pk__in = campaign_hoarding_query)

        serializer = CampaignSerializer(instance=campaign_query, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Hoarding
        fields = ('id', 'width', 'height', 'h_res', 'v_res', 'display_type', 'cost_cycle', 'cost', 'display_type', 'address', 'last_update', 'campaigns', )

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        hoarding = Hoarding.objects.create(address=address, user=self.context['request'].user, **validated_data)
        return hoarding

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        id = instance.address.id
        instance = Hoarding(**validated_data)
        instance.address = Address(**address_data)
        instance.address.id=id
        instance.address.save()
        # instance.save(ddress=instance.address)
        return instance




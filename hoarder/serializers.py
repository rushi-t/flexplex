from rest_framework import serializers
from hoarder.models import Hoarding, HoardingResource
from django.contrib.auth.models import User
from common.serializers import AddressSerializer
from common.models import Address

class HoardingResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoardingResource

class HoardingSerializer(serializers.HyperlinkedModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    address = AddressSerializer()

    class Meta:
        model = Hoarding
        fields = ('id', 'width', 'height', 'display_type', 'cost_cycle', 'cost', 'display_type', 'address', 'last_update' )

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




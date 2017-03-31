from rest_framework import serializers
from common import models
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from rest_auth.registration.serializers import RegisterSerializer
from models import UserProfile
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class RegSerializer(RegisterSerializer):
    phone = serializers.CharField(source="userprofile.phone")

    class Meta:
        fields = ('phone',)

    def custom_signup(self, request, user):
        profile_data = self.validated_data.pop('userprofile')
        profile = UserProfile.objects.create(user=user, **profile_data)
        profile.save()
        pass


class UserSerializer(UserDetailsSerializer):

    phone = serializers.CharField(source="userprofile.phone")

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('phone',)


    # def create(self, validated_data):
    #     profile_data = validated_data.pop('userprofile')
    #     profile = UserProfile.objects.create(**profile_data)
    #     user = UserModel.objects.create(**validated_data)
    #     user.save()
    #     profile.user=user
    #     profile.save()
    #     return profile

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        phone = profile_data.get('phone')

        instance = super(UserSerializer, self).update(instance, validated_data)

        # get and update user profile
        profile = instance.userprofile
        if profile_data and phone:
            profile.phone = phone
            profile.save()
        return instance




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

    class Meta:
        model = models.Address
        # fields = "__all__"
        exclude = ('id',)
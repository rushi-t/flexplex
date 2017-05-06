from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from rest_auth.registration.serializers import RegisterSerializer
from models import UserProfile
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import Group
import uuid
from quickstart.serializers import GroupSerializer

UserModel = get_user_model()

class RegSerializer(RegisterSerializer):
    phone = serializers.CharField(source="userprofile.phone")
    # password2 = serializers.CharField(source="password1")
    first_name = serializers.CharField()
    username = serializers.CharField()  # default=uuid.uuid4().hex[:8].upper())
    USER_TYPE_CHOICES = (
        (1, 'Advertiser'),
        (2, 'Hoarder'),
    )
    user_type = serializers.ChoiceField(choices=USER_TYPE_CHOICES)
    #users_group = Group.objects.get(name='advertiser')

    class Meta:
        model = UserProfile
        fields = ('first_name', 'phone',)

    def custom_signup(self, request, user):
        user_type = self.validated_data['user_type']
        setattr(user, 'first_name', self.validated_data['first_name'])
        #user['first_name'] = self.validated_data['first_name']
        user.save()
        profile_data = self.validated_data['userprofile']
        profile = UserProfile.objects.create(user=user, **profile_data)
        profile.save()
        request.user=user
        if user_type == 1:
            group = Group.objects.get(name='advertiser')
            user.groups.add(group)
        elif user_type == 2:
            group = Group.objects.get(name='hoarder')
            user.groups.add(group)
        pass

    def validate_password1(self, password):
        self._kwargs['data']._mutable=True
        self._kwargs['data']['password2'] = self._kwargs['data']['password1']
        return super(RegSerializer, self).validate_password1(password)

    def __init__(self, *args, **kwargs):
        self._kwargs['data']._mutable = True
        self._kwargs['data']['username'] = self._kwargs['data']['email']
        super(RegSerializer, self).__init__(*args, **kwargs)

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


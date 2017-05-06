from rest_framework import generics
from hoarder.models import Hoarding, HoardingResource
from hoarder.serializers import HoardingSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from django.views import View
from django.http import HttpResponseRedirect
from common.models import *
from advertiser.models import CampaignHoardings
from advertiser.serializers import CampaignHoardingsSerializer, CampaignSerializer

from datetime import datetime


# class CampaignViewSet(ModelViewSet):
#     queryset = Campaign.objects.all()
#     serializer_class = CampaignSerializer

class AllHoardingViewSet(ReadOnlyModelViewSet):
    #queryset = Hoarding.objects.all()
    serializer_class = HoardingSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        queryset = Hoarding.objects.all()
        if id != None:
            # update heartbeat
            hoarding = Hoarding.objects.get(id=id)
            hoarding.last_heartbeat = datetime.now()
            hoarding.save()
        return queryset


class MyHoardingViewSet(ModelViewSet):
    # queryset = Hoarding.objects.all()
    serializer_class = HoardingSerializer
    permission_classes = (IsAuthenticated,)

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        queryset = Hoarding.objects.filter(user=self.request.user)
        return queryset

#
# class CampaignHoardingFilter(django_filters.rest_framework.FilterSet):
#     class Meta:
#         model = CampaignHoardings
#         fields = ['campaign']


class CampaignHoardingsView(generics.ListAPIView):
    # queryset = CampaignHoardings.objects.filter(hoarding=1).only('hoarding')
    serializer_class = CampaignHoardingsSerializer
    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # filter_class = CampaignHoardingFilter

    def get_queryset(self):
        id = self.kwargs['id']
        queryset = CampaignHoardings.objects.filter(hoarding=id)
        # update heartbeat
        # hoarding = Hoarding.objects.get(id=id)
        # hoarding.last_heartbeat = datetime.now()
        # hoarding.save()
        return queryset


# class HoardingDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Hoarding.objects.all()
#     serializer_class = HoardingSerializer
#
#     # def pre_save(self, obj):
#     #     obj.user = self.request.user
#     def get(self, request):
#         queryset = Hoarding.objects.filter(id=self.request.GET.get('id', ''))
#         return render(request, 'hoarder/index.html', {'hoardings': queryset})


class HoarderHome(GenericAPIView):
    def get(self, request):
        hoardings = Hoarding.objects.filter(user=self.request.user)
        return render(request, 'hoarder/index.html', {'hoardings': hoardings})


class HoardingDetail(View):
    def get(self, request, id):
        hoarding = Hoarding.objects.get(user=self.request.user, id=id)
        campaigns = CampaignHoardings.objects.filter(hoarding=hoarding)
        return render(request, 'hoarder/hoarding-detail.html', {'hoarding': hoarding, 'campaigns': campaigns})

    def post(self, request, id):
        if request.POST.get('accept', False):
            id = int(request.POST['accept'])
            campaign = CampaignHoardings.objects.get(id=id)
            campaign.status = 1
            campaign.save()

        elif request.POST.get('reject', False):
            id = int(request.POST['reject'])
            campaign = CampaignHoardings.objects.get(id=id)
            campaign.status = 2
            campaign.save()
        return render(request, 'hoarder/hoarding-detail.html')


class AddHoardingView(View):
    def get(self, request):
        queryset = Hoarding.objects.all()
        return render(request, 'hoarder/add-hoarding.html', {'hoardings': queryset})

    def post(self, request, *args, **kwargs):
        address = Address(city=City.objects.get(id=request.POST['city']),
                          state=State.objects.get(id=request.POST['state']),
                          country=Country.objects.get(id=request.POST['country']),
                          address=request.POST['address'],
                          geo_location=request.POST['geo_location'])

        address.save()

        hoarding = Hoarding(user=self.request.user,
                            address=address,
                            width=request.POST['width'],
                            height=request.POST['height'],
                            display_type=request.POST['display_type'],
                            cost_cycle=request.POST['cost_cycle'],
                            cost=request.POST['cost'], )

        hoarding.save()
        return HttpResponseRedirect('../')


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
from advertiser.models import CampaignHoardings, CampaignImpressions, Campaign
from advertiser.serializers import CampaignHoardingsSerializer, CampaignSerializer
from advertiser import views

from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from datetime import date
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from emailcampaign.cron import email_scheduled_job

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
            hoarding.save(last_update=False)
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
        queryset = CampaignHoardings.objects.filter(hoarding=id).filter(status=CampaignHoardings.STATUS_TYPE_CHOICES[1][0]).\
            filter(Q(campaign__from_date__lte=date.today()) & Q(campaign__to_date__gte=date.today()))
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
    @method_decorator(login_required)
    def get(self, request):
        hoardings = Hoarding.objects.filter(user=self.request.user)
        #email_scheduled_job()
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
            campaign.hoarding.save()

        elif request.POST.get('reject', False):
            id = int(request.POST['reject'])
            campaign = CampaignHoardings.objects.get(id=id)
            campaign.status = 2
            campaign.save()
            campaign.hoarding.save()

        return render(request, 'hoarder/hoarding-detail.html')

class ActivateHoarding(View):
    def get(self, request, id):
        if self.request.user.is_superuser:
            hoarding = Hoarding.objects.get(id=id)
            hoarding.active_status = True
            hoarding.save()
            return HttpResponseRedirect('/hoarder')

class DeactivateHoarding(View):
    def get(self, request, id):
        if self.request.user.is_superuser:
            hoarding = Hoarding.objects.get(id=id)
            hoarding.active_status = False
            hoarding.save()
            return HttpResponseRedirect('/hoarder')

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
                            #cost_cycle=request.POST['cost_cycle'],
                            rate=request.POST['cost'],
                            start_time=datetime.strptime(request.POST['start_time'], '%I:%M %p').time(),
                            stop_time=datetime.strptime(request.POST['stop_time'], '%I:%M %p').time())

        if self.request.user.is_superuser:
            hoarding.active_status = True;

        hoarding.save()

        if request.FILES.get('resource') is not None:
            myfile = request.FILES['resource']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            hoardingResource = HoardingResource(hoarding=hoarding, resource=uploaded_file_url)
            hoardingResource.save()

        return HttpResponseRedirect('../')

class AddCampaign(View):
    def get(self, request, id):
        return render(request, 'hoarder/add-campaign.html',)

    def post(self, request, id):
        # hoarding = Hoarding.objects.get(user=self.request.user, id=id)
        post_values = request.POST.copy()
        post_values['hoardings'] = id
        request.POST = post_values
        views.create_campaign(request,CampaignHoardings.STATUS_TYPE_CHOICES[1][0])
        return HttpResponseRedirect('../')

class CampaignRequests(View):
    def get(self, request):
        campaignHoardings = CampaignHoardings.objects.filter(hoarding__user=self.request.user, status=CampaignHoardings.STATUS_TYPE_CHOICES[0][0]).order_by('-campaign__creation_date')
        return render(request, 'hoarder/campaign-requests.html', {'campaignHoardings': campaignHoardings})

    def post(self, request):
        if request.POST.get('accept', False):
            id = int(request.POST['accept'])
            campaign = CampaignHoardings.objects.get(id=id)
            campaign.status = 1
            campaign.save()
            campaign.hoarding.save()

        elif request.POST.get('reject', False):
            id = int(request.POST['reject'])
            campaign = CampaignHoardings.objects.get(id=id)
            campaign.status = 2
            campaign.save()
            campaign.hoarding.save()
        return render(request, 'hoarder/hoarding-detail.html')

class IncrementCampaignImprssion(View):
    def get(self, request, hoarding_id, campaign_id):
        campaignImpressions, created = CampaignImpressions.objects.get_or_create(hoarding_id=hoarding_id, campaign_id=campaign_id, date=date.today())
        campaignImpressions.impression_count += 1
        campaignImpressions.save()
        return HttpResponse(campaignImpressions.impression_count)


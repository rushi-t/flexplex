# views.py
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from advertiser.models import Campaign, CampaignHoardings
from advertiser.serializers import CampaignSerializer, CampaignResourceSerializer, CampaignHoardingsSerializer
from hoarder.models import Hoarding
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.utils.dateparse import parse_datetime
from django.core.files.storage import FileSystemStorage
from rest_auth.views import APIView


class CampaignResourceViewSet(ModelViewSet):
    # queryset = Campaign.objects.all()
    serializer_class = CampaignResourceSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        resource=self.request.data.get('resource'))

    def get_queryset(self):
        queryset = Campaign.objects.filter(user=self.request.user)
        return queryset


class CampaignViewSet(ModelViewSet):
    # queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    # parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        resource=self.request.data.get('resource'))

    def get_queryset(self):
        queryset = Campaign.objects.filter(user=self.request.user)
        return queryset


class CampaignHoardingsViewSet(ModelViewSet):
    # queryset = CampaignHoardings.objects.all()
    # queryset = CampaignHoardings.objects.none()
    serializer_class = CampaignHoardingsSerializer(many=True)

    def get_queryset(self):
        user = self.request.user
        campaigns = Campaign.objects.filter(user=user)
        return CampaignHoardings.objects.all()


class AdvertiserHome(APIView):
    def get(self, request):

        campaigns = Campaign.objects.filter(user=self.request.user)
        # for campaign in campaigns:
        #     hoardings = CampaignHoardings.objects.filter(campaign=campaign)
        #     campaign.hoardings['hoardings'] = hoardings

        return render(request, 'advertiser/index.html',
                      {'campaigns': campaigns })


class CreateCampaignView(View):
    def get(self, request):
        queryset = Hoarding.objects.all()
        return render(request, 'advertiser/campaign-wizard.html', {'hoardings': queryset})

    def post(self, request, *args, **kwargs):
        myfile = request.FILES['resource']
        fs = FileSystemStorage()
        filename = fs.save('static/uploads/' + myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        campaign = Campaign(user=self.request.user,
                            name=request.POST['name'],
                            from_date=request.POST['from_date'],
                            to_date=request.POST['to_date'],
                            resource=uploaded_file_url)
        campaign.save()
        for hoarding_id in request.POST.getlist('hoardings'):
            hoarding = Hoarding.objects.get(id=hoarding_id)
            CampaignHoardings.objects.create(campaign=campaign, hoarding=hoarding)
        return HttpResponseRedirect('../')

class CampaignDetail(View):
    def get(self, request, id):
        campaign = Campaign.objects.get(id=id)
        return render(request, 'advertiser/campaign-detail.html', {'campaign': campaign})

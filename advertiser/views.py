# views.py
import os
from subprocess import call

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from advertiser.models import Campaign, CampaignHoardings
from advertiser.serializers import CampaignSerializer, CampaignResourceSerializer, CampaignHoardingsSerializer
from hoarder.models import Hoarding, get_active_hoardings
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.utils.dateparse import parse_datetime
from django.core.files.storage import FileSystemStorage
from rest_auth.views import APIView
from datetime import datetime
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
    @method_decorator(login_required)
    def get(self, request):
        campaigns = Campaign.objects.filter(user=self.request.user).order_by('-to_date')
        # for campaign in campaigns:
        #     hoardings = CampaignHoardings.objects.filter(campaign=campaign)
        #     campaign.hoardings['hoardings'] = hoardings

        email = EmailMessage('Subject', 'Body', to=['rushikesh.talokar@gmail.com'])
        email.send()

        # subject, from_email, to = 'Html Test', 'admin@flexplex.in ', 'rushikesh.talokar@gmail.com'
        #
        # html_content = render_to_string('email/cerberus-responsive.html', {'varname': 'value'})  # ...
        # text_content = strip_tags(html_content)  # this strips the html, so people will have the text as well.
        #
        # # create the email, and attach the HTML version as well.
        # msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=[to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()

        return render(request, 'advertiser/index.html',
                      {'campaigns': campaigns})


def create_campaign(request, status=CampaignHoardings.STATUS_TYPE_CHOICES[0][0]):
    myfile = request.FILES['resource']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        outFileName = os.path.splitext(filename)[0] + '.mp4'


        ffmpegCmd = 'ffmpeg -loop 1 -i ' \
                    + fs.location + "/" + filename + ' -c:v libx264 -t 10 -pix_fmt yuv420p -vf scale=1280:720 ' \
                    + fs.location + "/" + outFileName
        # local

        # ffmpegCmd = 'ffmpeg -loop 1 -i ' \
        #             + fs.location + "/" + filename + ' -c:v libx264 -t 10 -pix_fmt yuv420p -vf scale=1280:720 ' \
        #             + fs.location + "/" + outFileName
        process = call(ffmpegCmd, shell=True)

        ##AVI File
        aviFileName = os.path.splitext(filename)[0] + '.avi'
        ffmpegCmd = 'ffmpeg -i ' \
                    + fs.location + "/" + outFileName + ' -vcodec mpeg4 ' \
                    + fs.location + "/" + aviFileName
        process = call(ffmpegCmd, shell=True)

        # process.wait()
        filename = outFileName

    uploaded_file_url = fs.url(filename)

    campaign = Campaign(user=request.user,
                        name=request.POST['name'],
                        from_date=request.POST['from_date'],
                        to_date=request.POST['to_date'],
                        resource=uploaded_file_url)
    campaign.save()
    for hoarding_id in request.POST.getlist('hoardings'):
        hoarding = Hoarding.objects.get(id=hoarding_id)
        CampaignHoardings.objects.create(campaign=campaign, hoarding=hoarding, status=status)
        hoarding.save()


class CreateCampaignView(View):
    def get(self, request):
        queryset = get_active_hoardings()
        return render(request, 'advertiser/campaign-wizard.html', {'hoardings': queryset})

    def post(self, request, *args, **kwargs):
        create_campaign(request)
        return HttpResponseRedirect('../')


class CampaignDetail(View):
    def get(self, request, id):
        campaign = Campaign.objects.get(id=id)
        return render(request, 'advertiser/campaign-detail.html', {'campaign': campaign})


class Inventory(GenericAPIView):
    def get(self, request):
        queryset = get_active_hoardings()
        return render(request, 'advertiser/inventory.html', {'hoardings': queryset})

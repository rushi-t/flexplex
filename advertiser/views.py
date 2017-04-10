# views.py
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from advertiser.models import Campaign, CampaignHoardings
from advertiser.serializers import CampaignSerializer,CampaignResourceSerializer, CampaignHoardingsSerializer


class CampaignResourceViewSet(ModelViewSet):
    #queryset = Campaign.objects.all()
    serializer_class = CampaignResourceSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        resource=self.request.data.get('resource'))

    def get_queryset(self):
        queryset = Campaign.objects.filter(user=self.request.user)
        return queryset

class CampaignViewSet(ModelViewSet):
    #queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    #parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        resource=self.request.data.get('resource'))

    def get_queryset(self):
        queryset = Campaign.objects.filter(user=self.request.user)
        return queryset

class CampaignHoardingsViewSet(ModelViewSet):
    #queryset = CampaignHoardings.objects.all()
    #queryset = CampaignHoardings.objects.none()
    serializer_class = CampaignHoardingsSerializer(many=True)

    def get_queryset(self):
        user = self.request.user
        campaigns = Campaign.objects.filter(user=user)
        return CampaignHoardings.objects.all()

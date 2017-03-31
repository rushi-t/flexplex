# views.py
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from advertiser.models import Campaign, CampaignHoardings
from advertiser.serializers import CampaignSerializer, CampaignHoardingsSerializer


class CampaignViewSet(ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        resource=self.request.data.get('resource'))


class CampaignHoardingsViewSet(ModelViewSet):
    queryset = CampaignHoardings.objects.all()
    serializer_class = CampaignHoardingsSerializer

from rest_framework import generics
from hoarder.models import Hoarding
from hoarder.serializers import HoardingSerializer
from rest_framework.viewsets import ModelViewSet

# class CampaignViewSet(ModelViewSet):
#     queryset = Campaign.objects.all()
#     serializer_class = CampaignSerializer

class HoardingViewSet(ModelViewSet):
    queryset = Hoarding.objects.all()
    serializer_class = HoardingSerializer

    def pre_save(self, obj):
        obj.user = self.request.user

class HoardingDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Hoarding.objects.all()
    serializer_class = HoardingSerializer

    # def pre_save(self, obj):
    #     obj.user = self.request.user
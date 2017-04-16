from rest_framework import generics
from hoarder.models import Hoarding
from hoarder.serializers import HoardingSerializer
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
# class CampaignViewSet(ModelViewSet):
#     queryset = Campaign.objects.all()
#     serializer_class = CampaignSerializer

class AllHoardingViewSet(ReadOnlyModelViewSet):
    queryset = Hoarding.objects.all()
    serializer_class = HoardingSerializer

    def pre_save(self, obj):
        obj.user = self.request.user

class MyHoardingViewSet(ModelViewSet):
    #queryset = Hoarding.objects.all()
    serializer_class = HoardingSerializer
    permission_classes = (IsAuthenticated,)

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        queryset = Hoarding.objects.filter(user=self.request.user)
        return queryset

class HoardingDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Hoarding.objects.all()
    serializer_class = HoardingSerializer

    # def pre_save(self, obj):
    #     obj.user = self.request.user
    def get(self, request):
        queryset = Hoarding.objects.filter(id=self.request.GET.get('id', ''))
        return render(request, 'hoarder/index.html', {'hoardings': queryset})


class HoarderHome(GenericAPIView):
    def get(self, request):
        queryset = Hoarding.objects.filter(user=self.request.user)
        return render(request, 'hoarder/index.html', {'hoardings': queryset})
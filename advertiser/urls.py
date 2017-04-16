from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from common import views
from django.conf.urls import include
from rest_framework import routers
from django.views.generic import TemplateView
from views import CampaignViewSet, CampaignResourceViewSet,\
    CampaignHoardingsViewSet, AdvertiserHome, CreateCampaignView
from models import Campaign, CampaignHoardings

router = routers.DefaultRouter()
router.register(r'campaign', CampaignViewSet, Campaign)
router.register(r'resource', CampaignResourceViewSet, Campaign)
router.register(r'campaign-hoardings', CampaignHoardingsViewSet,CampaignHoardings)
urlpatterns = router.urls

urlpatterns = [

    url(r'create/campaign$', CreateCampaignView.as_view()),
    url(r'api/', include(router.urls)),
    url(r'', AdvertiserHome.as_view()),
    # url(r'ad-upload/', TemplateView.as_view(template_name='file-upload.html')),
    # url(r'create-campaign/', TemplateView.as_view(template_name='create-campaign.html')),
    # url(r'choose-hoarding/', TemplateView.as_view(template_name='choose-hoarding.html')),

]

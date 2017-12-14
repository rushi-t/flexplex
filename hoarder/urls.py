from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from common import views
from django.conf.urls import include
from rest_framework import routers
from django.views.generic import TemplateView
from views import AllHoardingViewSet,MyHoardingViewSet, \
    HoarderHome, HoardingDetail, AddHoardingView, CampaignHoardingsView, AddCampaign, \
    IncrementCampaignImprssion, CampaignRequests, ActivateHoarding, DeactivateHoarding, HideHoarding

router = routers.DefaultRouter()
router.register(r'all/hoardings', AllHoardingViewSet, base_name="Hoarding")
router.register(r'my/hoardings', MyHoardingViewSet, base_name="Hoarding")
#router.register(r'hoarding/(?P<id>\d+)/campaigns$', CampaignHoardingsView, base_name="Campaign")
urlpatterns = router.urls

urlpatterns = [

    url(r'add/hoarding/$', AddHoardingView.as_view()),
    url(r'edit/hoarding/(?P<id>\d+)/$', AddHoardingView.as_view()),
    url(r'delete/hoarding/(?P<id>\d+)/$', HideHoarding.as_view()),
    url(r'hoarding/(?P<id>\d+)/$', HoardingDetail.as_view()),
    url(r'hoarding/(?P<id>\d+)/add/campaign', AddCampaign.as_view()),
    url(r'hoarding/(?P<id>\d+)/activate', ActivateHoarding.as_view()),
    url(r'hoarding/(?P<id>\d+)/deactivate', DeactivateHoarding.as_view()),
    url(r'hoarding/(?P<hoarding_id>\d+)/increment/campaign/(?P<campaign_id>\d+)', IncrementCampaignImprssion.as_view()),
    url(r'campaign/requests$', CampaignRequests.as_view()),
    url(r'/api/hoarding/(?P<id>\d+)/campaigns', CampaignHoardingsView.as_view()),


    # url(r'hoarding/', HoardingDetail.as_view()),
    # url(r'register/', TemplateView.as_view(template_name='register-hoarding.html')),
    # url(r'location/', TemplateView.as_view(template_name='location.html')),
    url(r'/api/', include(router.urls)),
    url(r'/$', HoarderHome.as_view()),


]

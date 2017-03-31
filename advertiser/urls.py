from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from common import views
from django.conf.urls import include
from rest_framework import routers
from django.views.generic import TemplateView
from views import CampaignViewSet, CampaignHoardingsViewSet

router = routers.DefaultRouter()
router.register(r'campaign', CampaignViewSet)
router.register(r'campaign-hoardings', CampaignHoardingsViewSet)
urlpatterns = router.urls

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'ad-upload/', TemplateView.as_view(template_name='file-upload.html')),
]

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from common import views
from django.conf.urls import include
from rest_framework import routers
from django.views.generic import TemplateView
from views import HoardingViewSet

router = routers.DefaultRouter()
router.register(r'hoarding', HoardingViewSet)
urlpatterns = router.urls

urlpatterns = [
    url(r'^', include(router.urls)),
]

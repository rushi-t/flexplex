from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from common import views
from django.conf.urls import include
from rest_framework import routers
from django.views.generic import TemplateView
from views import AllHoardingViewSet,MyHoardingViewSet

router = routers.DefaultRouter()
router.register(r'all/hoardings', AllHoardingViewSet, base_name="Hoarding")
router.register(r'my/hoardings', MyHoardingViewSet, base_name="Hoarding")
urlpatterns = router.urls

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'home/', TemplateView.as_view(template_name='hoarder/index.html')),
    url(r'add/', TemplateView.as_view(template_name='hoarder/add-hoarding.html')),
    url(r'register/', TemplateView.as_view(template_name='register-hoarding.html')),
    url(r'location/', TemplateView.as_view(template_name='location.html')),
]

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from common import views
from django.conf.urls import include
from rest_framework import routers
from django.views.generic import TemplateView
from views import AllHoardingViewSet,MyHoardingViewSet, \
    HoarderHome, HoardingDetail, AddHoardingView

router = routers.DefaultRouter()
router.register(r'all/hoardings', AllHoardingViewSet, base_name="Hoarding")
router.register(r'my/hoardings', MyHoardingViewSet, base_name="Hoarding")
urlpatterns = router.urls

urlpatterns = [

    url(r'/add/hoarding$', AddHoardingView.as_view()),
    url(r'/hoarding/(?P<id>\d+)/$', HoardingDetail.as_view()),

    # url(r'hoarding/', HoardingDetail.as_view()),
    # url(r'register/', TemplateView.as_view(template_name='register-hoarding.html')),
    # url(r'location/', TemplateView.as_view(template_name='location.html')),
    # url(r'api/', include(router.urls)),
    url(r'/$', HoarderHome.as_view()),

]

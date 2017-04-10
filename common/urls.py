from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from common import views
from django.conf.urls import include
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'city', views.CityViewSet)
router.register(r'state', views.StateViewSet)
router.register(r'country', views.CountryViewSet)
router.register(r'address', views.AddressViewSet)
urlpatterns = router.urls
urlpatterns = [
    url(r'^', include(router.urls)),
]

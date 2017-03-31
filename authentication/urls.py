from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from common import views
from django.conf.urls import include
from rest_framework import routers


router = routers.DefaultRouter()
urlpatterns = router.urls
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/register/', include('rest_auth.registration.urls')),
]

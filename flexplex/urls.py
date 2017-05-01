from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin
from quickstart import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
#from hoarder.views import HoardingDetail, HoardingList

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^common/', include('common.urls')),
    url(r'advertiser', include('advertiser.urls')),
    url(r'hoarder', include('hoarder.urls')),
    url(r'', include('authentication.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
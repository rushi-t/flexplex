from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from authentication import views
from django.conf.urls import include
from rest_framework import routers
from django.views.generic import TemplateView
from views import SigninView
from models import UserProfile
from django.contrib.auth.views import logout

router = routers.DefaultRouter()
#router.register(r'signin', SigninView, UserProfile)
urlpatterns = router.urls
urlpatterns = [
    url(r'^$', views.HomeView.as_view()),
    url(r'^', include(router.urls)),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/register/', include('rest_auth.registration.urls')),
    url(r'^signin/$', views.SigninView.as_view()),
    url(r'^activation-pending/$', views.UserActivationPendingView.as_view()),
    url(r'^register/$', views.MyRegisterView.as_view()),
    # url(r'^logout/$', 'logout',
    #                       {'next_page': '/successfully_logged_out/'}),
    # url(r'/', TemplateView.as_view(template_name='index.html')),

    #url(r'auth/', TemplateView.as_view(template_name='auth.html')),
]

from django.conf.urls import include
from django.conf.urls import url

from views import EmailCampaignRead
urlpatterns = [
    url(r'email/campaign/(?P<id>\d+)/read', EmailCampaignRead.as_view()),
]

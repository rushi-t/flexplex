# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.shortcuts import render
from django.views import View
from emailcampaign import models
from django.http import HttpResponse

# Create your views here.

PIXEL_GIF_DATA = """
R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
""".strip().decode('base64')

class EmailCampaignRead(View):
    def get(self, request, id):
        campaign_user = models.CampaignUser.objects.get(id=id)
        campaign_user.is_read = True
        campaign_user.save()
        #return HttpResponse("")

        transparant_img_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + \
                                "/static/img/transparant-1px.png"
        image_data = open(transparant_img_path, "rb").read()
        return HttpResponse(image_data, content_type='image/png')

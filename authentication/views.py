from common import models
from rest_framework import viewsets
from common import serializers
from rest_framework.response import Response
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render

from rest_auth.views import LoginView

class SigninView(LoginView):

    def get(self,request):
        return render(request,'auth.html')

    def post(self, request, *args, **kwargs):
        response = super(SigninView, self).post(request, *args, **kwargs)
        user = request.user
        if user.groups.filter(name='advertiser').exists():
            return HttpResponseRedirect("../advertiser")
        else:
            return HttpResponseRedirect("../hoarder")
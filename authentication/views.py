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
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)

from rest_auth.views import LoginView
from rest_auth.registration.views import RegisterView
from forms import LoginForm, RegisterForm

from models import UserProfile

def logout(request):
    try:
        request.user.auth_token.delete()
    except:
        pass

    django_logout(request)

class HomeView(View):
    def get(self, request):
        user = request.user
        # if request.user.is_authenticated:
        #     if user.groups.filter(name='advertiser').exists():
        #         return HttpResponseRedirect("../advertiser")
        #     else:
        #         return HttpResponseRedirect("../hoarder")
        # else:
        #     return render(request, 'index.html')
        return render(request, 'index.html')

class SigninView(LoginView):

    def get(self,request):
        return render(request,'auth.html')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, 'auth.html', {'form': form})
        else:
            response = super(SigninView, self).post(request, *args, **kwargs)
            user = request.user
            profile = UserProfile.objects.get(user=user)
            if profile is None or profile.is_activated() is True:
                if user.groups.filter(name='advertiser').exists():
                    return HttpResponseRedirect("../advertiser")
                else:
                    return HttpResponseRedirect("../hoarder")
            else:
                logout(request)
                return HttpResponseRedirect("/activation-pending/")

class MyRegisterView(RegisterView):

    def get(self, request):
        return render(request, 'auth.html')

    def post(self, request, *args, **kwargs):

        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, 'auth.html', {'register_form': form})
        else:
            response = super(MyRegisterView, self).post(request, *args, **kwargs)
            logout(request)
            return HttpResponseRedirect("/register/success")
            # user = request.user
            # if user.groups.filter(name='advertiser').exists():
            #     return HttpResponseRedirect("/advertiser?first_login=true")
            # else:
            #     return HttpResponseRedirect("/hoarder?first_login=true")

class UserActivationPendingView(View):
    def get(self, request):
        return render(request, 'user_activation_pending.html')

class PostRegistrationView(View):
    def get(self, request):
        return render(request, 'post_registration_page.html')
from django.shortcuts import render,redirect
from django.views import generic
from django.shortcuts import render
from django.contrib.auth import views
from django.contrib.auth import login, logout,authenticate
from .forms import TenantForm,TenantLoginForm
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Tenant
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class RentInHome(generic.TemplateView):
    template_name ='accounts/base.html'

class RentInRegisterVIew(generic.CreateView):
    form_class = TenantForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

class TenantLoginView(views.LoginView):
    form_class = TenantLoginForm
    template_name ='registration/login.html'
    success_url = reverse_lazy('home')
class ProfileDetailView(generic.DetailView, LoginRequiredMixin):
    model = Tenant
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'tenant'
    def get_object(self, queryset=None):
        # Retrieve the current logged-in user's profile
        return self.request.user.tenant  # Adjust this line if your model relationships differ
class ProfileUpdateView(generic.UpdateView, LoginRequiredMixin):
    model =Tenant
    form_class =TenantForm
    context_object_name = 'tenant'
    template_name = 'accounts/profile_update.html'
    success_url =reverse_lazy('profile')
    def get_object(self, queryset=None):
        # Retrieve the current logged-in user's profile
        return self.request.user.tenant 
    
class AccountLogoutView(views.LogoutView):
    template_name='accounts/logged_out.html'
    # success_url = 'login'
    
    
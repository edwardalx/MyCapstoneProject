from django.shortcuts import render,redirect
from django.views import generic
from django.shortcuts import render
from django.contrib.auth import views
from django.contrib.auth import login, logout,authenticate
from .forms import TenantForm,TenantLoginForm,TenantUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .models import Tenant
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets,generics,status
from .serializers import TenantSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import permissions
# Create your views here.

User = get_user_model()
class RentInHome(generic.TemplateView):
    template_name ='accounts/base.html'

class RentInRegisterVIew(generic.CreateView):
    form_class = TenantForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

class TenantLoginView(views.LoginView):
    form_class = TenantLoginForm
    template_name ='registration/login.html'
    success_url = reverse_lazy('profile')
class ProfileDetailView(LoginRequiredMixin, generic.DetailView ):
    model = Tenant
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'tenant'
    def get_object(self, queryset=None):
        # Retrieve the current logged-in user's profile
        return self.request.user.tenant  # Adjust this line if your model relationships differ
class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model =Tenant
    form_class = TenantUpdateForm
    context_object_name = 'tenant'
    template_name = 'accounts/profile_update.html'
    success_url =reverse_lazy('profile')
    def get_object(self, queryset=None):
        # Retrieve the current logged-in user's profile
        return self.request.user.tenant 
   
class AccountLogoutView(views.LogoutView):
    template_name='accounts/logged_out.html'

    # success_url = 'login'
    

class TenantApiViewset(viewsets.ModelViewSet):
    model = Tenant
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes =[permissions.IsAuthenticated]

class TenantRegisterApi(generics.CreateAPIView):
    model =Tenant
    queryset = Tenant.objects.all()
    serializer_class =TenantSerializer

# This code is not even needed as simple will handle login and logoutjwt
class  TenantLoginAPIView(generics.GenericAPIView):   
    def post(self ,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'username': user.username,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        

# if you use both JWT & sessions, you may want both logout mechanisms.
@method_decorator(csrf_exempt, name='dispatch')
class LogoutAPIView(generic.View):
    def post(self, request):
        # Logout from Django session
        logout(request)
        
        # Blacklist refresh token if provided
        refresh_token = request.POST.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                return JsonResponse({'error': 'Invalid token'}, status=400)
        
        return JsonResponse({'message': 'Logged out successfully'})
    

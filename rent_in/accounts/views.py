from django.contrib import messages
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
from .serializers import TenantSerializer, PhoneTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from my_properties.models import Property
# Create your views here.

User = get_user_model()
class RentInHome(generic.TemplateView):
    template_name = 'accounts/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = Property.objects.all()
        return context

class RentInRegisterVIew(generic.CreateView):
    form_class = TenantForm
    template_name = 'accounts/new_register.html'
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "✅ Registration successful! You can now log in.")
        return response

class TenantLoginView(views.LoginView):
    form_class = TenantLoginForm
    template_name ='registration/login.html'
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
    

class PhoneLoginView(TokenObtainPairView):
    serializer_class = PhoneTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # Only handle JWT token response — no session login
        return super().post(request, *args, **kwargs)

@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid credentials'}, status=401)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]  # Important: don't require auth to log out
    def post(self, request):
        # Try to blacklist refresh token
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass  # Ignore if already blacklisted or invalid

        # # Fully clear session if user is logged in
        # if request.user.is_authenticated:
        #     logout(request)
        #     request.session.flush()

        return Response(status=status.HTTP_205_RESET_CONTENT)

def check_user_or_email(request):
    username = request.GET.get('username')
    email = request.GET.get('email')

    if username:
        exists = Tenant.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})
    
    if email:
        exists = Tenant.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})
    
    return JsonResponse({'exists': False})
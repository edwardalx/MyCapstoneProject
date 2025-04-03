
from django.urls import path, include
from .views import RentInHome,RentInRegisterVIew,TenantLoginView,ProfileDetailView,AccountLogoutView, AccountApiViewset,TenantRegisterApi,TenantLoginAPIView
from django.contrib.auth import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profile',AccountApiViewset)
urlpatterns=[
    path('', view=RentInHome.as_view(), name='home'),
    path('login/', view=TenantLoginView.as_view(template_name ='registration/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='accounts/logged_out.html'), name='logout'),
    # path('logout/', AccountLogoutView.as_view(), name='logout'),
    path('register/', view=RentInRegisterVIew.as_view(), name='register' ),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile-update/', ProfileDetailView.as_view(), name='edit_profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Password Change
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('api/register/', view=TenantRegisterApi.as_view(),name='register-api' ),
   path('api/login/', view=TenantLoginAPIView.as_view(), name='login-api'),
   path('api/', include(router.urls)),
]

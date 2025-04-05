from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TenancyApiViewset
router = DefaultRouter()
router.register(r'profile',TenancyApiViewset)



urlpatterns = [
path('api/tenacy', include(router.urls)),
]
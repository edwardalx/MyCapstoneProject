from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PaymentApiViewset
router = DefaultRouter()
router.register(r'profile',PaymentApiViewset)



urlpatterns = [
path('api/', include(router.urls)),
]
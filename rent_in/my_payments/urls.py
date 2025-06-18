from rest_framework.routers import DefaultRouter
from django.urls import path, include
from my_payments import views
router = DefaultRouter()
router.register(r'history',views.PaymentSummaryApiViewset)
router.register(r'payments',views.PaymentApiViewset)



urlpatterns = [
path('api/', include(router.urls)),
path('webhook/', views.paystack_webhook, name='paystack_webhook'),
path('api/initialize/', views.initialize_payment, name='initialize_payment'),
path('verify/<str:reference>/', views.verify_payment, name='verify_payment'),
path('make-payment/', views.payment_page, name='make_payment'),
path('payment-history/', views.payment_history, name='payment_history'),
path('receipt/<str:reference>/', views.payment_receipt, name='payment_receipt'),
]
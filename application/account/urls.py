from django.urls import path
from .views import LoginView, RegisterView, PaymentView, CheckOutView, PaymentSettingsView

app_name = 'account'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('checkout/', CheckOutView.as_view(), name="checkout"),
    path('payment_settings/', PaymentSettingsView.as_view(), name="payment_settings"),
]

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator as Min


class Customer(AbstractUser):
    # Customer Information
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    organization = models.CharField(max_length=50)
    website = models.URLField()
    # Billing Information
    billing_start_date = models.DateTimeField(blank=True, null=True)
    # Braintree API Information
    braintree_customer_id = models.CharField(max_length=200, blank=True, null=True)
    braintree_subscription_id = models.CharField(max_length=200, blank=True, null=True)
    # Google Ads API Information
    google_ads_customer_id = models.CharField(max_length=50, blank=True, null=True)

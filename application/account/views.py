from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.views import View
from .forms import CustomerForm, LoginForm
from .models import Customer
from application.api.braintree_api import Customer, Subscription, Transaction, PaymentMethod
import logging


class LoginView(View):
    template_name = "account/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse("Authenticated")
        return render(request, self.template_name)


class RegisterView(View):
    template_name = "account/register.html"

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse("Authenticated")
        customer_form = CustomerForm()
        return render(request, self.template_name, {'form': customer_form})

    def post(self, request):
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            return HttpResponse("Authenticated")
        return render(request, self.template_name, {'form': customer_form})


class PaymentView(View):
    template_name = "account/payment.html"

    def get(self, request):
        new_customer = Customer()
        client_token = new_customer.GATEWAY.client_token.generate()
        return render(request, self.template_name, {'client_token': client_token})

    def post(self, request):
        new_customer = Customer()
        new_subscription = Subscription()
        nonce_from_the_client = request.POST["payment_method_nonce"]
        creation = new_customer.create_customer(nonce_from_the_client)
        print(creation.is_success)

        if not creation.is_success:
            print("Unable to create customer")
            return redirect(reverse("account:login"))

        elif creation.is_success:
            customer_id = creation.customer.id
            print("Here is the customer's id: " + str(customer_id))
            customer_token = creation.customer.payment_methods[0].token
            create_subscription = new_subscription.create_subscription(customer_token)
            if create_subscription.is_success:
                customer_subscription_id = create_subscription.subscription.id
                print("Subscription has been made")
                print("Here is the customer's id: " + str(customer_id))
                print("Billing day of the month: " + str(create_subscription.subscription.billing_day_of_month))
                print("Here is the customer's subscription id: " + str(customer_subscription_id))
                return redirect(reverse("account:checkout"))


class CheckOutView(View):
    template_name = "account/checkout.html"

    def get(self, request):
        return render(request, self.template_name)


class PaymentSettingsView(View):
    template_name = "account/payment_settings.html"

    def get(self, request):
        existing_customer = Customer()
        dict_client = {
            'customer_id': '577619089',
            'options': {
                'make_default': True,
            }
        }

        client_token = existing_customer.GATEWAY.client_token.generate(dict_client)
        return render(request, self.template_name, {'client_token': client_token})

    def post(self, request):
        customer = Customer()
        method = PaymentMethod()
        customer_subscription = Subscription()
        nonce_from_the_client = request.POST['payment_method_nonce']
        existing_customer, customer_payment_method = customer.find_customer('577619089')

        # check if the customer's default payment method is verified
        for item in customer_payment_method:
            if item.default:
                verification = item.verifications[0]['status']
                print(verification)
                # if verified, continue to transaction
                if verification == 'verified':
                    continue
                else:
                    print("Credit card is invalid.  Please choose another payment method")

        create_method = method.create_payment_method('577619089', nonce_from_the_client)
        if create_method.is_success:
            payment_method_token = create_method.payment_method.token
            new_default_payment_method = method.update_payment_method(payment_method_token)
            if new_default_payment_method:
                print("Updated new default payment method token to: " + payment_method_token)
                # len(existing_customer.customer.credit_cards)

        # subscription_update = customer_subscription.update_subscription(
        #     request.user.braintree.subscription_id,
        #     transaction_payment_method_token,
        #     request.user.budget0    # Replace price with request.user.budget0
        # )
        # Check if both the subscription and payment_method were updated.
        #     if payment_method_update.is_success:
        #         print("Successfully changed default payment method.")
        #         # print("New default payment method is now: " + transaction_payment_method_token)
        #         # print("New monthly budget is now: " + request.user.budget0)
        #     else:
        #         print("Error: Either the subscription or the default payment method unsuccessfully updated")

        return HttpResponse("New Default has been set")





"""
Finding customer by ID: customer = gateway.customer.find("the_customer_id")
========================================================

Deleting payment method for recurring billing system: 
result = gateway.payment_method.delete("the_token").

result.is_success
# True

========================================================
Getting number of credit_cards from customer:
len(result.customer.credit_cards)

========================================================
Determining which payment method is the default:
customer = gateway.customer.find("the_customer_id")
customer.payment_methods # array of braintree.PaymentMethod instances
payment_method.default # finds customer's default payment method
"""



from django.test import TestCase, Client
from django.shortcuts import reverse
from .forms import CustomerForm, LoginForm
from .models import Customer


class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_unauthenticated(self):
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated(self):
        """ This should redirect authenticated users to somewhere else."""
        customer = Customer(
            name="Elon Musk",
            email="elon@tesla.com",
            organization="Tesla",
            website="https://www.tesla.com/"
        )
        customer.save()
        self.client.force_login(customer)
        response = self.client.get(reverse('account:login'))
        content = response.content.decode("utf-8")
        self.assertEqual(content, "Authenticated")


class TestRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_unauthenticated(self):
        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated(self):
        """ This should redirect authenticated users to somewhere else."""
        customer = Customer(
            name="Elon Musk",
            email="elon@tesla.com",
            organization="Tesla",
            website="https://www.tesla.com/"
        )
        customer.save()
        self.client.force_login(customer)
        response = self.client.get(reverse('account:register'))
        content = response.content.decode("utf-8")
        self.assertEqual(content, "Authenticated")


class TestCustomerForm(TestCase):
    def test_valid(self):
        data = {
            'name': "Elon Musk",
            'email': "elon@tesla.com",
            'organization': "Tesla",
            'website': "https://www.tesla.com/",
            'password1': "Tesla-is-awesome-2020",
            'password2': "Tesla-is-awesome-2020"
        }
        customer_form = CustomerForm(data=data)
        self.assertTrue(customer_form.is_valid())

    def test_invalid_empty_data(self):
        customer_form = CustomerForm(data={})
        self.assertFalse(customer_form.is_valid())

    def test_invalid_empty_fields(self):
        data = {
            'name': "",
            'email': "",
            'organization': "",
            'website': "",
            'password1': "",
            'password2': ""
        }
        customer_form = CustomerForm(data=data)
        self.assertFalse(customer_form.is_valid())

    def test_invalid_short_password(self):
        data = {
            'name': "Elon Musk",
            'email': "elon@tesla.com",
            'organization': "Tesla",
            'website': "https://www.tesla.com/",
            'password1': "Elon123",
            'password2': "Elon123"
        }
        customer_form = CustomerForm(data=data)
        self.assertFalse(customer_form.is_valid())

    def test_invalid_password_mismatch(self):
        data = {
            'name': "Elon Musk",
            'email': "elon@tesla.com",
            'organization': "Tesla",
            'website': "https://www.tesla.com/",
            'password1': "Tesla-is-awesome-2020",
            'password2': "Ford-sucks-2020"
        }
        customer_form = CustomerForm(data=data)
        self.assertFalse(customer_form.is_valid())

    def test_invalid_email(self):
        data = {
            'name': "Elon Musk",
            'email': "Elon Musk is an awesome email.",
            'organization': "Tesla",
            'website': "https://www.tesla.com/",
            'password1': "Tesla-is-awesome-2020",
            'password2': "Tesla-is-awesome-2020"
        }
        customer_form = CustomerForm(data=data)
        self.assertFalse(customer_form.is_valid())

    def test_invalid_website(self):
        data = {
            'name': "Elon Musk",
            'email': "elon@tesla.com",
            'organization': "Tesla",
            'website': "Elon Musk is an awesome website.",
            'password1': "Tesla-is-awesome-2020",
            'password2': "Tesla-is-awesome-2020"
        }
        customer_form = CustomerForm(data=data)
        self.assertFalse(customer_form.is_valid())

    def test_invalid_input_size(self):
        size = 50
        data = {
            'name': "Elon Musk" * size,
            'email': "elon@tesla.com",
            'organization': "Tesla" * size,
            'website': "https://www.tesla.com/",
            'password1': "Tesla-is-awesome-2020",
            'password2': "Tesla-is-awesome-2020"
        }
        customer_form = CustomerForm(data=data)
        self.assertFalse(customer_form.is_valid())

    def test_invalid_email_exists(self):
        existing_email = "elon@tesla.com"
        customer = Customer(
            name="Elon Musk",
            email=existing_email,
            organization="Tesla",
            website="https://www.tesla.com/"
        )
        customer.save()
        data = {
            'name': "Bill Gates",
            'email': existing_email,
            'organization': "Microsoft",
            'website': "https://www.microsoft.com/en-us/",
            'password1': "Microsoft-is-awesome-2020",
            'password2': "Microsoft-is-awesome-2020"
        }
        customer_form = CustomerForm(data=data)
        self.assertFalse(customer_form.is_valid())


class TestCustomerModel(TestCase):
    def test_model_creation(self):
        name = "Elon Musk"
        customer = Customer(
            name=name,
            email="elon@tesla.com",
            organization="Tesla",
            website="https://www.tesla.com/"
        )
        customer.save()
        self.assertEqual(customer.name, name)

    def test_nonprofit_billing_start_date(self):
        # TODO: Finish implementing.
        self.assertTrue(True)


class TestBraintree(TestCase):
    def setUp(self):
        self.client = Client()

    def test_subscription_made_success(self):
        credit_card_data = {
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
            },
            "payment_method_nonce": 'fake-valid-nonce',
            "options": {
                "submit_for_settlement": "true"
            }
        }
        transaction_response = self.client.post(reverse("account:payment"), credit_card_data)
        self.assertEqual(transaction_response.status_code, 302)

    def test_subscription_made_unsuccessful(self):
        credit_card_data = {
            "credit_card": {
                "number": "4000111111111115",
                "expiration_date": "12/34",
            },
            "payment_method_nonce": 'fake-processor-declined-visa-nonce',
            "options": {
                'submit_for_settlement': True
            }
        }
        response = self.client.post(reverse("account:payment"), credit_card_data)
        self.assertEqual(response.status_code, 302)

    def test_null_fields(self):
        credit_card_data = {
            "credit_card": {
                "number": "",
                "expiration_date": "",
            },
            "payment_method_nonce": 'fake-valid-nonce',
            "options": {
                'submit_for_settlement': True
            }
        }
        response = self.client.post(reverse("account:payment"), credit_card_data)
        self.assertEqual(response.status_code, 302)

    def test_invalid_payment_method_in_payment_settings(self):
        credit_card_data = {
            "credit_card": {
                "number": "4000111111111115",
                "expiration_date": "12/34"
            },
            "payment_method_nonce": "fake-valid-nonce"
        }
        response = self.client.post(reverse("account:payment_settings"), credit_card_data)
        self.assertEqual(response.status_code, 302)

import braintree

GATEWAY = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="xfq6by3vkhvbxjgg",
        public_key="gry63cfkp2hjj4fw",
        private_key="3fca027417ef4b7183f68dd222e35392"
    )
)
PLAN_ID = "p35m"


class Transaction:
    global GATEWAY

    def __init__(self):
        self.GATEWAY = GATEWAY

    def create_transaction(self, nonce_from_the_client):
        result = self.GATEWAY.transaction.sale({
            "amount": "10.00",
            "payment_method_nonce": nonce_from_the_client,
            "options": {
                "submit_for_settlement": True
            }
        })
        return result


class Customer:
    def __init__(self):
        self.GATEWAY = GATEWAY

    def create_customer(self, nonce_from_the_client):
        result = self.GATEWAY.customer.create({
            "first_name": "Kristian",
            "last_name": "Rolland",
            "payment_method_nonce": nonce_from_the_client,
        })
        return result

    def update_customer(self, id, token):
        result = self.GATEWAY.customer.update(id, {
            "default_payment_method_token": token,
            "credit_card": {
                "options": {
                    "update_existing_token": token
                }
            }
        })
        return result

    def find_customer(self, id):
        customer = self.GATEWAY.customer.find(id)
        customer_payment_method = customer.payment_methods
        return customer, customer_payment_method


class PaymentMethod:
    def __init__(self):
        self.GATEWAY = GATEWAY

    def create_payment_method(self, id, nonce_from_the_client):
        result = self.GATEWAY.payment_method.create({
            "customer_id": id,
            "payment_method_nonce": nonce_from_the_client
        })
        return result

    def update_payment_method(self, token):
        result = self.GATEWAY.payment_method.update(token, {
            "options": {
                "make_default": True,
            }
        })
        return result

    def delete_payment_method(self, token):
        result = self.GATEWAY.payment_method.delete(token)
        return result


class Subscription:
    def __init__(self):
        self.GATEWAY = GATEWAY
        self.PLAN_ID = PLAN_ID

    def create_subscription(self, token):
        result = self.GATEWAY.subscription.create({
            "payment_method_token": token,
            "plan_id": self.PLAN_ID,
            "billing_day_of_month": 1
        })
        return result

    def update_subscription(self, subscription_id, token, new_price):
        result = self.GATEWAY.subscription.update(subscription_id, {
            "payment_method_token": token,
            "price": new_price,
        })
        return result

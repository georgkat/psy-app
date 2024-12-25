import datetime

import stripe

TEST_API_KEY = 'sk_test_51QRWM7JTAo4CmwBPUfv30HMSnlyTXed77hAP7CA7IroDSCIOYm6BivbfaXsHr6ciHsvkW8Tm9iG7j5X5ZinJ1SvZ00boDkTZUN'

stripe.api_key = TEST_API_KEY

def create_customer(customer_mail, customer_name):
    stripe.Customer.create(
        email=customer_mail,
        name=customer_name
    )
    return True

def new_card():
    pass

def create_charge(ammount=19500*100, source='tok_visa', description='test_payment'):
    stripe.Charge.create(
        amount=ammount,
        currency="HUF",
        source=source,
        description=description,
        capture=False
        # capture_before=datetime.datetime.now() + datetime.timedelta(12)
    )

def capture_charge():
    for item in stripe.Charge.list():
        try:
            stripe.Charge.capture(item['id'])
            print(f'{item["id"]} captured')
        except:
            print(f'{item["id"]} not captured')
    return True

def return_charges():
    charges = stripe.Charge.list()
    return charges

def return_balance():
    balance = stripe.Balance.retrieve()
    return balance
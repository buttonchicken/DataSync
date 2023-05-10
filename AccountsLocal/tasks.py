import stripe
from DataSync.settings import STRIPE_SECRET_KEY
import shortuuid
from AccountsLocal.models import UserLocal
from DataSync.celery import app
stripe.api_key = STRIPE_SECRET_KEY

'''create a customer'''
@app.task(bind=True)
def create_customer_stripe(self,data):
    try:
        existing_cutomer = stripe.Customer.list(email=data['email'])
        if len(existing_cutomer)>0:
            return {'error':'Customer with same email exists!'}
        cust = stripe.Customer.create(
               id = data['id'],
               name = data['name'],
               email = data['email']
               )
        return cust
    except Exception as e:
        self.retry(countdown=2, exc=e, max_retries=5)
        return {'error':str(e)}

'''fetch a list of stripe customers'''
def get_all_customers_stripe():
    customer_list = stripe.Customer.list()
    return customer_list

'''update a customer'''
@app.task(bind=True)
def update_customer_stripe(self,data):
    try:
        cust = stripe.Customer.modify(
                data['id'],
                name = data['name'], 
                email = data['email']
                )
        return cust
    except Exception as e:
        self.retry(countdown=2, exc=e, max_retries=5)
        return {'error':str(e)}

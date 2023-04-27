from celery import shared_task
import stripe
from DataSync.settings import STRIPE_SECRET_KEY
import shortuuid
from AccountsLocal.models import UserLocal

stripe.api_key = STRIPE_SECRET_KEY

'''create a customer'''
@shared_task()
def create_customer_stripe(data,id_required = False):
    # try:
    #     st = stripe.Customer.search(query='email:'+str(data['email']).strip(' ')+' AND '+'name:'+ str(data['name']).strip(' '))
    #     print(st)
    #     return {'error':'Customer already exists'}
    # except:
    try:
        if id_required:
            cust = stripe.Customer.create(
                        id = shortuuid.uuid()[:10],
                        name = data['name'],
                        email = data['email']
                    )
        else:
            cust = stripe.Customer.create(
                        id = data['id'],
                        name = data['name'],
                        email = data['email']
                    )
        return cust
    except Exception as e:
        return {'error':str(e)}

def get_all_customers_stripe():
    customer_list = stripe.Customer.list()
    return customer_list

'''update a customer'''
@shared_task()
def update_customer_stripe(data):
    try:
        cust = stripe.Customer.modify(
                data['id'],
                name = data['name'], 
                email = data['email']
                )
        return cust
    except Exception as e:
        return {'error':str(e)}

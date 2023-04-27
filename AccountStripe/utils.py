import stripe
from DataSync.settings import STRIPE_SECRET_KEY
import shortuuid

stripe.api_key = STRIPE_SECRET_KEY

'''create a customer'''
def create_customer(data):
    # try:
    #     st = stripe.Customer.search(query='email:'+str(data['email']).strip(' ')+' AND '+'name:'+ str(data['name']).strip(' '))
    #     print(st)
    #     return {'error':'Customer already exists'}
    # except:
    try:
        cust = stripe.Customer.create(
                    id = shortuuid.uuid()[:10],
                    name = data['name'],
                    email = data['email']
                )
        return cust
    except Exception as e:
        return {'error':str(e)}

def get_all_customers():
    customer_list = stripe.Customer.list()
    return customer_list

'''update a customer'''
def update_customer(data):
    try:
        cust = stripe.Customer.modify(
                data['id'],
                name = data['name'], 
                email = data['email']
                )
        return cust
    except:
        return {'error':'data not valid'}
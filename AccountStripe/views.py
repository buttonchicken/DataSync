from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import stripe
from DataSync.settings import STRIPE_SECRET_KEY
import shortuuid
from .tasks import create_user_local, update_user_local
from AccountsLocal.tasks import get_all_customers_stripe

class CreateUserStripe(APIView):
    def post(self,request):
       stripe.api_key = STRIPE_SECRET_KEY
       data = request.data
       data['id']=shortuuid.uuid()[:10]
       try:
        cust = stripe.Customer.create(
                            id = data['id'],
                            name = data['name'],
                            email = data['email']
                        )
        create_user_local.delay(data)
        return Response(cust,status=status.HTTP_200_OK)
       except Exception as e:
          return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
class UpdateUserStripe(APIView):
    def put(self,request,id=None):
        try:
            data = request.data
            if 'name' in data.keys() and 'email' in data.keys():
                cust = stripe.Customer.modify(
                        id,
                        name = data['name'], 
                        email = data['email']
                        )
                data['id']=id
                update_user_local.delay(data)
                return Response(cust,status=status.HTTP_200_OK)
            elif 'name' in data.keys() and 'email' not in data.keys():
               cust = stripe.Customer.modify(
                       id,
                       name = data['name'], 
                       )
               data['id']=id
               update_user_local.delay(data)
               return Response(cust,status=status.HTTP_200_OK)
            else:
               cust = stripe.Customer.modify(
                       id,
                       email = data['email'], 
                       )
               data['id']=id
               update_user_local.delay(data)
               return Response(cust,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class FetchStripeUsers(APIView):
   def get(self,request):
      try:
        all_customers = get_all_customers_stripe()
        return Response(all_customers,status=status.HTTP_200_OK)
      except Exception as e:
         return Response({'error':e},status=status.HTTP_400_BAD_REQUEST)
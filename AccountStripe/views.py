from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import stripe
from DataSync.settings import STRIPE_SECRET_KEY
import shortuuid
from .tasks import create_user_local, update_user_local

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
          return Response({'error':str(e)})
        
class UpdateUserStripe(APIView):
    def put(self,request,id=None):
        try:
            data = request.data
            cust = stripe.Customer.modify(
                    id,
                    name = data['name'], 
                    email = data['email']
                    )
            data['id']=id
            update_user_local.delay(data)
            return Response(cust,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)})
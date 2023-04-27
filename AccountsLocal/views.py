from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from .models import UserLocal
from .tasks import *

class CreateUserDB(APIView):
    def post(self,request):
        name = request.data['name']
        email = request.data['email']
        if len(UserLocal.objects.filter(name=name,email=email))>0:
            return Response({'message':'User already Exists!'},status=status.HTTP_400_BAD_REQUEST)
        else:
            if 'id' in request.data.keys():
                usr_obj = UserLocal.objects.create(id=request.data['id'],name=name,email=email)
            else:
                usr_obj = UserLocal.objects.create(name=name,email=email)
            create_customer_stripe.delay(UserDisplaySerializer(usr_obj).data)
            serialized_obj = UserDisplaySerializer(usr_obj).data
            return Response({'message':'User Created Successfully','payload':serialized_obj},status=status.HTTP_200_OK)

class UpdateUserDB(APIView):
    def put(self,request,id=None):
        usr_obj = UserLocal.objects.get(id=id)
        serializer = UpdateSerializer(usr_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            update_customer_stripe.delay(serialized_data)
            return Response({'message':'User Updated Successfully','payload':serialized_data},status=status.HTTP_200_OK)
        else:
            return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class FetchLocalUsers(APIView):
    def get(self,request):
        try:
            usr_obj = UserLocal.objects.all()
            serializer = UserDisplaySerializer(usr_obj, many=True)
            serialized_data = serializer.data
            return Response(serialized_data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
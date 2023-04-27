from AccountsLocal.models import UserLocal
from django.db import transaction
from celery import shared_task
from AccountsLocal.serializers import UserDisplaySerializer,UpdateSerializer

@shared_task()
@transaction.atomic
def create_user_local(data):
    try:
        usr = UserLocal.objects.create(id = data['id'], name = data['name'], email = data['email'])
        serialized_data = UserDisplaySerializer(usr).data
        return serialized_data
    except Exception as e:
        return {'error':str(e)}

@shared_task()
@transaction.atomic
def update_user_local(data):
    try:
        usr_obj = UserLocal.objects.get(id = data['id'])
        serializer = UpdateSerializer(usr_obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return serialized_data
        else:
            return {'error':'Error in updating'}
    except Exception as e:
        return {'error':str(e)}
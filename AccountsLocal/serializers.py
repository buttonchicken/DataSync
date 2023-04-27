from .models import UserLocal
from rest_framework import serializers

class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocal
        fields = ['id','name','email']
    
class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocal
        fields = ['id','name','email']
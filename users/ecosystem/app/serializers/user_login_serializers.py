from rest_framework import serializers
from users.models import *
import os

env = os.getenv
        
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = [
            'pk',
            'created'
        ]
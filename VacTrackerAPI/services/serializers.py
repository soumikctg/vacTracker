from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'name', 'phone', 'password', 'userType', 'nid', 'address']
        extra_kwargs = {
            'password': {'write_only': True}
        }

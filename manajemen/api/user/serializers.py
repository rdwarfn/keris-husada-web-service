from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from manajemen.models import User

class UserSerializer(serializers.ModelSerializer):
    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)
    
    class Meta:
        model = User
        fields = '__all__'


class CustomTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

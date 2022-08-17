from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'nickname']

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        nickname = validated_data.get('nickname')

        hashed_password = make_password(password=password)

        user = User(email=email, password=hashed_password, nickname=nickname)
        user.save()

        return {'email': email, 'nickname': nickname}
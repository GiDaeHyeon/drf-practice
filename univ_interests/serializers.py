from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
import jwt
from datetime import datetime, timedelta
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


class SignInSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['email']

    def login(self, user, input_password):
        if check_password(input_password, user.password):
            payload = {'user_id': user.id, 'exp': datetime.now() + timedelta(seconds=60 * 60)}
            token = jwt.encode(payload, 'SECRET', 'HS256')
            return token
        else:
            return False

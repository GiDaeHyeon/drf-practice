from django.db.utils import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
import jwt
from datetime import datetime, timedelta
from .models import User, University, Country, UniversityPreference


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


class CountrySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'code']


class UniversitySearchSerializer(serializers.ModelSerializer):
    country = CountrySearchSerializer(read_only=True)

    class Meta:
        model = University
        fields = ['id', 'name', 'webpage', 'country']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name']


class UniversityPreferenceSerializer(serializers.ModelSerializer):
    user = UserSerializer
    university = UniversitySerializer

    class Meta:
        model = UniversityPreference
        fields = ['university']

    def create(self, user):
        university = self.validated_data.get('university')

        try:
            preference = UniversityPreference(user=user, university=university)
            preference.save()
        except IntegrityError:
            return False

        return {'user': user.id, 'university': university.name}

    def update(self, user):
        university = self.validated_data.get('university')

        try:
            target_instance = UniversityPreference.objects.get(user=user, university=university, deleted_at__isnull=True)
        except UniversityPreference.DoesNotExist:
            return False

        target_instance.deleted_at = datetime.now()
        target_instance.save()
        return True

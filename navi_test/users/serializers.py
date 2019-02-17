import requests
from pyhunter import PyHunter

from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    def validate(self, data):
        """
        Validate email existance using hunter.io service
        """
        email = data.get('email')
        if email:
            hunter = PyHunter(settings.EMAIL_HUNTER_API_KEY)
            """
            acc_info used to determine if my account still have available api calls,
            however it always return same number
            link: https://hunter.io/api/v2/docs#account
            """
            acc_info = requests.get(f'https://api.hunter.io/v2/account?api_key={settings.EMAIL_HUNTER_API_KEY}')
            print(acc_info.json()['data'])

            if acc_info.json()['data']['calls']['available'] < 1:
                return data

            email_data = hunter.email_verifier(email)

            if email_data.get('result') == 'undeliverable':
                raise ValidationError('Email address does not exist')

        return data

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


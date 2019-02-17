from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings
from pyhunter import PyHunter

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


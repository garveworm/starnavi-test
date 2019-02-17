from rest_framework import serializers, exceptions
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from .models import Post, Like


User = get_user_model()


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'post', 'user')
        read_only_fields = ('user',)

    def create(self, validated_data):
        user_id = self.context.get('request').user.id
        validated_data['user'] = User.objects.get(id=user_id)
        try:
            like = super().create(validated_data)
        except IntegrityError:
            raise exceptions.ValidationError('Integrity Error: fields post,'
                                             ' user should make a unique set')

        return like


class PostSerializer(serializers.ModelSerializer):
    like_set = LikeSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('title', 'body', 'like_set')

    def create(self, validated_data):
        user_id = self.context.get('request').user.id
        validated_data['user'] = User.objects.get(id=user_id)
        post = super().create(validated_data)

        return post


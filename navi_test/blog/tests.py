from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


from .models import Post, Like

User = get_user_model()


class TestPosts(APITestCase):

    def setUp(self):
        self.user_data = {"username": "som", "email": "som@gmail.com", "password": "password"}
        User.objects.create_user(**self.user_data)
        # self.user = self.client.post(reverse('signup'), self.user_data)
        self.token = self.client.post(reverse('login'), self.user_data).data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_user_can_create_post(self):
        post_data = {"title": "post_title"}
        response = self.client.post(reverse('post-list'), post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.all()[0]
        self.assertEqual(post.title, post_data['title'])


class TestLikes(APITestCase):

    def setUp(self):
        self.user_data = {"username": "som", "email": "som@gmail.com", "password": "password"}
        User.objects.create_user(**self.user_data)
        # self.client.post(reverse('signup'), self.user_data)
        self.user = User.objects.all()[0]
        self.token = self.client.post(reverse('login'), self.user_data).data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        post_data = {"title": "post_title"}
        self.client.post(reverse('post-list'), post_data)
        self.post = Post.objects.all()[0]

    def test_user_can_like_post(self):
        like_data = {"post": self.post.id, "user": self.user.id}
        response = self.client.post(reverse('like-list'), like_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post.like_set.count(), 1)

    def test_user_can_like_post_only_once(self):
        like_data = {"post": self.post.id, "user": self.user.id}
        self.client.post(reverse('like-list'), like_data)
        response = self.client.post(reverse('like-list'), like_data)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_delete_like(self):
        like_data = {"post": self.post.id, "user": self.user.id}
        response = self.client.post(reverse('like-list'), like_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        like_id = Like.objects.all()[0].id
        response = self.client.delete(reverse('like-detail', kwargs={"pk":like_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)




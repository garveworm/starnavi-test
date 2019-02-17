from django.db import models
from django.conf import settings


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey('users.User', null=True, on_delete=models.SET_NULL)


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('post', 'user')


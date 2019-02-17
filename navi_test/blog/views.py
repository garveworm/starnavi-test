from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


from .serializers import PostSerializer, LikeSerializer
from .models import Post, Like
# Create your views here.


class PostViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikeViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Like.objects.all()
    serializer_class = LikeSerializer



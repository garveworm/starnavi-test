from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'posts', viewset=views.PostViewSet)
router.register(r'likes', viewset=views.LikeViewSet)

urlpatterns = router.urls


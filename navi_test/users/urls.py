from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from . import views


urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('token-obtain/', obtain_jwt_token, name='token_obtain_pair'),
    path('token-refresh/', refresh_jwt_token, name='token_refresh'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('signup/', views.SignupUserView.as_view(), name='signup')
]

from django.contrib.auth import authenticate, login

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.settings import api_settings

from .serializers import UserSerializer, TokenSerializer, UserLoginSerializer


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#
class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({"message":"hello"})


class LoginUserView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        user = authenticate(request, username=username, password=password)

        print(username, password, user, authenticate)

        if user:
            login(request, user)
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            serializer = TokenSerializer(data={'token':token})
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_401_UNAUTHORIZED)


class SignupUserView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer





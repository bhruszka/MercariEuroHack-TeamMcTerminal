import requests
from django.conf import settings
from django.contrib.auth import login, logout, get_user_model
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

# Create your views here.


# Login ApiView
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import LoginSerializer, CreateUserSerializer, UserSerializer, FacebokLoginSerializer

app_name = 'api'


class LoginApiView(CreateAPIView):
    """Log in using Api"""
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.login()
            if user:
                login(request, user)
                return Response(status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(RetrieveAPIView):

    def get_queryset(self):
        return get_user_model().objects.filter(id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(('You have logged out successfully.'))


class LoginFacebookView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FacebokLoginSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            request_url = 'https://graph.facebook.com/me/?access_token={}&client_id={}&client_secret={}&grant_type={}'.format(
                serializer.validated_data['access_token'],
                settings.SOCIAL_AUTH_FACEBOOK_KEY,
                settings.SOCIAL_AUTH_FACEBOOK_SECRET,
                'id,kupa'
            )
            response = requests.get(request_url)
        return Response(status=status.HTTP_400_BAD_REQUEST,data='BŁAD')

class CreateUser(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()
    queryset = get_user_model().objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user_model()(username=serializer.validated_data['username'], is_active=True,
                                email=serializer.validated_data['email'])
        user.set_password(serializer.validated_data['password'])
        user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(id=self.request.user.id)

    def get_object(self):
        return self.get_queryset().get(id=self.request.user.id)

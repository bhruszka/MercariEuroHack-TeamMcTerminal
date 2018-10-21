import json
import tempfile
import uuid

from io import StringIO, BytesIO
from uuid import uuid4

import requests
from django.conf import settings
from django.contrib.auth import login, logout, get_user_model
from django.core import files
from django.db.models import Case, When, Value, CharField, Q
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

# Create your views here.


# Login ApiView
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import LoginSerializer, CreateUserSerializer, UserSerializer, FacebokLoginSerializer, \
    RouteSerializer
from carpool_matcher.models import Route
from carpool_matcher.utils import get_polyline_from_path

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
                res = Response(status.HTTP_202_ACCEPTED)
                res.set_cookie('sessionid', request.session.session_key)
                return res
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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            request_url = 'https://graph.facebook.com/me/?access_token={}&client_id={}&client_secret={}&grant_type=client_credentials&fields=id,name,email'.format(
                serializer.validated_data['token'],
                settings.SOCIAL_AUTH_FACEBOOK_KEY,
                settings.SOCIAL_AUTH_FACEBOOK_SECRET
            )
            response = json.loads(requests.get(request_url).text)
            if response['id'] != serializer.validated_data['userId']:
                return Response(status=status.HTTP_400_BAD_REQUEST, data='Bad userId')
            try:
                user = get_user_model().objects.get(facebook_id=serializer.validated_data['userId'])
            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create(first_name=response['name'].split(' ')[0],
                                                       last_name=response['name'].split(' ')[1],
                                                       email=response['email'],
                                                       username=response['email'],
                                                       facebook_id=serializer.validated_data['userId'])
                image_url = 'https://graph.facebook.com/{}/picture?access_token={}&client_id={}&client_secret={}&grant_type=client_credentialsŁ'.format(
                    serializer.validated_data['userId'],
                    serializer.validated_data['token'],
                    settings.SOCIAL_AUTH_FACEBOOK_KEY,
                    settings.SOCIAL_AUTH_FACEBOOK_SECRET
                )

                request = requests.get(image_url, stream=True)

                # Get the filename from the url, used for saving later
                file_name = "{}.{}".format(uuid.uuid4(), request.headers.get('content-type').split('/')[1])

                # Create a temporary file
                lf = tempfile.NamedTemporaryFile()

                # Read the streamed image in sections
                for block in request.iter_content(1024 * 8):

                    # If no more file then stop
                    if not block:
                        break

                    # Write image block to temporary file
                    lf.write(block)

                # Save the temporary image to the model#
                # This saves the model so be sure that is it valid
                user.avatar.save(file_name, files.File(lf))
                user.save()
            user.facebook_token = serializer.validated_data['token']
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data='BŁAD')


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

    @list_route(methods=['GET'])
    def your_profile(self, request, *args, **kwargs):
        return Response(self.serializer_class(request.user).data)


# class RouteFilter(filters.FilterSet):
#     type = filters.CharFilter(name='type', method='filter_type')
#
#     class Meta:
#         model = Route
#         fields = {
#         }
#
#     def filter_type(self, qs, name, value):
#         lookup_expr = ''
#         if value == 'passenger':
#             lookup_expr = "driver__user"
#         if value == 'driver':
#             lookup_expr = "passenger__user"
#         if lookup_expr == '':
#             return qs
#         return qs.exclude(**{lookup_expr: self.request.user})


class RouteViewSet(ModelViewSet):
    """
    type - either 'driver' or 'passenger' for query and for post

    start_point and end_point are of format {"longitude": "","latitude":""}
    """
    serializer_class = RouteSerializer
    # filter_backends = (DjangoFilterBackend,)
    pagination_class = None

    # filter_class = RouteFilter

    def get_queryset(self):
        value = self.request.query_params.get('value')
        qs = Route.objects.all()
        lookup_expr = ''
        if value == 'passenger':
            lookup_expr = "driver__user"
        if value == 'driver':
            lookup_expr = "passenger__user"
        if lookup_expr != '':
            qs.exclude(**{lookup_expr: self.request.user})
        return qs.annotate(
            type=Case(When(Q(driver__isnull=False), then=Value('driver')), output_field=CharField(),
                      default=Value('passenger'))).filter(
            (
                    (
                            Q(passenger__isnull=False) and Q(passenger__user=self.request.user)
                    ) |
                    (
                            Q(driver__isnull=False) and Q(driver__user=self.request.user)
                    )
            )
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @list_route(methods=['GET'])
    def all_routes(self, request, *args, **kwargs):
        queryset = Route.objects.all().annotate(
            type=Case(When(Q(driver__isnull=False), then=Value('driver')), output_field=CharField(),
                      default=Value('passenger'))).filter(type='driver')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @list_route(methods=['GET'])
    def path(self, request, *args, **kwargs):
        if request.user.drivers.all().count():
            return Response({"poly_line": get_polyline_from_path(request.user.drivers.first().path)},
                            status=status.HTTP_200_OK)
        if request.user.passengers.all().count():
            return Response({"poly_line": get_polyline_from_path(request.user.passengers.first().path)},
                            status=status.HTTP_200_OK)
        return Response({"poly_line": None}, status=status.HTTP_200_OK)

    @list_route(methods=['GET'])
    def passengers(self, request, *args, **kwargs):
        if request.user.drivers.all().count() > 0:
            return Response(request.user.drivers.first().passengers.all().values_list('user__username', flat=True),
                            status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from carpool_matcher.models import Location, Route, Driver, Passenger


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        # model = User
        fields = ('username', 'password')

    def login(self):
        username = self.initial_data['username']
        password = self.initial_data['password']
        user = authenticate(username=username, password=password)
        return user


class FacebokLoginSerializer(serializers.Serializer):
    token = serializers.CharField()
    userId = serializers.CharField()

    class Meta:
        fields = ('token', 'userId')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')

    def validate(self, attrs):
        if get_user_model().objects.filter(email=attrs['email']).exists():
            raise TypeError('Email aleady in use')
        if get_user_model().objects.filter(username=attrs['username']).exists():
            raise TypeError('Username not unique')
        # TODO: Password validation
        return attrs


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    password_new = serializers.CharField(required=False)
    avatar = serializers.ImageField(read_only=True)
    http_method_names = ['put', 'patch', 'get', ]

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password_new', 'avatar')

    def update(self, instance, validated_data):
        if validated_data.get('password_new'):
            instance.set_password(validated_data.get['password_new'])
            del validated_data['password_new']
        super().update(instance, validated_data)

    def validate(self, attrs):
        # TODO: Password validation
        return attrs


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'longitude', 'latitude')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'avatar', 'first_name')


class RouteSerializer(serializers.ModelSerializer):
    start_point = LocationSerializer()
    end_point = LocationSerializer()
    path = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    type = serializers.CharField(required=False)

    class Meta:
        model = Route
        fields = ('id', 'start_point', 'end_point', 'type', 'path','users')


    def get_path(self, obj):
        if hasattr(obj, 'type'):
            if obj.type == 'driver':
                return LocationSerializer(obj.driver.path, many=True).data
            if obj.type == 'passenger':
                return LocationSerializer(obj.passenger.path, many=True).data
        return None

    def get_users(self, obj):
        if hasattr(obj, 'type'):
            if obj.type == 'driver':
                return UserSerializer(obj.driver.path_users, many=True).data
            if obj.type == 'passenger':
                return UserSerializer(obj.passenger.path_users, many=True).data
        return None

    def create(self, validated_data):
        if validated_data.get('start_point'):
            location = Location(
                longitude=validated_data['start_point']['longitude'],
                latitude=validated_data['start_point']['latitude']
            )
            location.save()
            validated_data['start_point'] = location
        if validated_data.get('end_point'):
            location = Location(
                longitude=validated_data['end_point']['longitude'],
                latitude=validated_data['end_point']['latitude']
            )
            location.save()
            validated_data['end_point'] = location
        if validated_data.get('type'):
            request = self.context['request']
            if validated_data['type'] == 'driver':
                try:
                    driver = Driver.objects.get(user=request.user)
                except Driver.DoesNotExist:
                    driver = Driver(user=request.user)
                    driver.save()
                validated_data['driver'] = driver
            elif validated_data['type'] == 'passenger':
                try:
                    passenger = Passenger.objects.get(user=request.user)
                except Passenger.DoesNotExist:
                    passenger = Passenger(user=request.user)
                    passenger.save()
                validated_data['passenger'] = passenger
            del validated_data['type']
        return super().create(validated_data)

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


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
    access_token = serializers.CharField()
    user_id = serializers.CharField()

    class Meta:
        fields = ('access_token', 'user_id')


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

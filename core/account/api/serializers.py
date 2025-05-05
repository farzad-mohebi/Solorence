from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model

from account.models import User
from utils.serializer import CustomSerializer


class UserSerializer(CustomSerializer):
    class Meta:
        model = User
        fields = model.serializer_fields()

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def validate_password(self, value):
        if self.context['view'].action == 'create':
            data = self.get_initial()
            password = data.get('password')
            if password is None or password == '':
                raise serializers.ValidationError('Password is required!')
        return make_password(value)


class UserProfileSerializer(CustomSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']


class UserSignUpSerializer(CustomSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'first_name', 'last_name']

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['username'] = validated_data['email'].split('@')[0]
        return super(UserSignUpSerializer, self).create(validated_data)

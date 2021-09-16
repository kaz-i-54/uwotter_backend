from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers

from .models import MyUser
# from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = MyUser
        fields = ('id', 'name', 'password')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = MyUser
        fields = ('id', 'name')
        read_only_fields = ('id',)

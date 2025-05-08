# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')
    def create(self, validated_data):
        validated_data['role'] = 'customer'
        return User.objects.create_user(**validated_data)

class DataEntrySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    def create(self, validated_data):
        validated_data['role'] = 'data_entry'
        user = User.objects.create_user(**validated_data)
        return user


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
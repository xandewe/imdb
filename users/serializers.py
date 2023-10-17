from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import CustomUser
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=['email'],
                message="email already exists"
            )
        ]

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        ...

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
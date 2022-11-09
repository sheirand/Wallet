from rest_framework import serializers
from user.models import User
from user.services import AuthenticationService

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'balance', 'birthdate', 'categories')


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(max_length=32, write_only=True, required=True)
    token = serializers.CharField(read_only=True, max_length=255)

    class Meta:
        model = User
        fields = ("email", "password", "token")

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = AuthenticationService.authenticate(email=email, password=password)

        attrs['user'] = user

        return attrs

    def create(self, validated_data):
        user = validated_data.get("user")
        token = AuthenticationService.create_jwt_token(user_id=user.id, user_email=user.email)
        return {"token": token}

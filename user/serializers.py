from rest_framework import serializers
from user.models import User, Categories
from user.services import AuthenticationService, DEFAULT_CATEGORIES
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="User with this email already exists"
            )
        ]
    )
    password = serializers.CharField(max_length=32, write_only=True, required=True)
    balance = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    categories = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'balance', 'categories')

    def create(self, validated_data):
        validated_data['categories'] = []
        for category in DEFAULT_CATEGORIES:
            category = Categories.objects.get_or_create(name=category)[0]
            validated_data['categories'].append(category.id)
        return super().create(validated_data)


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(max_length=32, write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "password")


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

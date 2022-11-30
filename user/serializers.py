from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user.models import Categories, User
from user.services import DEFAULT_CATEGORIES, AuthenticationService


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
        password = validated_data.pop('password')
        for category in DEFAULT_CATEGORIES:
            category = Categories.objects.get_or_create(name=category)[0]
            validated_data['categories'].append(category.id)
        user = super().create(validated_data)
        user.set_password(raw_password=password)
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    balance = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    categories = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Categories.objects.all())

    class Meta:
        model = User
        fields = ("email", "balance", "categories")

    def to_internal_value(self, data):
        for cat in data.get('categories', []):
            Categories.objects.get_or_create(name=cat)
        return super().to_internal_value(data)


class LoginSerializer(serializers.ModelSerializer):
    """Authorization and token obtain serializer"""
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(max_length=32, write_only=True, required=True)
    token = serializers.CharField(read_only=True, max_length=255)

    class Meta:
        model = User
        fields = ("email", "password", "token")

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = AuthenticationService.creds_authenticate(email=email, password=password)

        attrs['user'] = user

        return attrs

    def create(self, validated_data):
        user = validated_data.get("user")
        token = AuthenticationService.create_jwt(user_id=user.id, user_email=user.email)
        return {"token": token}


class ChangePwSerializer(serializers.ModelSerializer):
    """Serializer for changing password"""
    email = serializers.EmailField(read_only=True)
    password = serializers.CharField(max_length=32, write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "password")


class UserStatsSerializer(serializers.Serializer):
    """Serializer for simple user's stats"""
    category = serializers.CharField(source="category__name")
    count = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=15, decimal_places=2, source="sum")

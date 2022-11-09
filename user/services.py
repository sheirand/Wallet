import datetime
from rest_framework import exceptions
from user.models import User
from django.conf import settings
import jwt


class AuthenticationService:

    @staticmethod
    def authenticate(email: str, password: str) -> "User":

        user = User.objects.get(email=email)

        if not user:
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        return user

    @staticmethod
    def create_jwt_token(user_id: int, user_email: str) -> str:
        """Service for creating jwt"""
        payload = dict(
            id=user_id,
            email=user_email,
            iat=datetime.datetime.utcnow(),
            exp=datetime.datetime.utcnow() + datetime.timedelta(minutes=40)
        )
        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

        return token

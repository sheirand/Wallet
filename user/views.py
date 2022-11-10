from rest_framework import viewsets, mixins
from user.models import User
from user.serializers import UserSerializer, LoginSerializer


class UserApiViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginViewset(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

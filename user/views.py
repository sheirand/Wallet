from rest_framework import viewsets, mixins, permissions
from user.models import User
from user.permissions import IsOwnerOrAdmin
from user.serializers import UserSerializer, LoginSerializer, RegistrationSerializer


class UserApiViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = (permissions.IsAdminUser,)
        elif self.action == 'create':
            permission_classes = (permissions.AllowAny,)
        else:
            permission_classes = (IsOwnerOrAdmin,)
        return [permission() for permission in permission_classes]


class UserLoginViewset(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

from django.db.models import Count, Sum
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User
from user.permissions import IsOwnerOrAdmin
from user.serializers import (ChangePwSerializer, LoginSerializer,
                              UserDetailSerializer, UserSerializer,
                              UserStatsSerializer)
from wallet.models import Transaction


class UserApiViewset(viewsets.ModelViewSet):
    """User Model Viewset"""
    queryset = User.objects.all().prefetch_related("categories")

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return UserSerializer
        elif self.action in ("password",):
            return ChangePwSerializer
        else:
            return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = (permissions.IsAdminUser,)
        elif self.action == 'create':
            permission_classes = (permissions.AllowAny,)
        else:
            permission_classes = (IsOwnerOrAdmin,)
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(request_body=ChangePwSerializer, responses={
        200: '{"detail": "password was changed successfully"}'}
                         )
    @action(detail=True, methods=['put'], name='change-password', url_path="change-password",
            permission_classes=(IsOwnerOrAdmin,), serializer_class=ChangePwSerializer)
    def password(self, request, pk, *args, **kwargs):
        """Changing password extra-action"""
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "password was changed successfully"}, status=status.HTTP_200_OK)


class UserLoginViewset(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    """User authorization (token obtain) view"""
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)


class UserStats(mixins.ListModelMixin,
                viewsets.GenericViewSet):
    """Viewset for simple user-profile statistics"""
    serializer_class = UserStatsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Transaction.objects.filter(user__id=self.request.user.id).\
            values("category__name").annotate(count=Count("id"), sum=Sum("amount"))
        return queryset

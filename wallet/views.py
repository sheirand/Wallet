from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from user.permissions import IsOwnerOrAdmin
from user.models import User
from wallet.models import Transaction
from wallet.serializers import TransactionSerializer


class TransactionAPIViewset(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # updating user's balance
        user = User.objects.get(id=self.request.user.id)
        if instance.income:
            user.balance -= instance.amount
        else:
            user.balance += instance.amount
        user.save()
        return super().perform_destroy(instance)

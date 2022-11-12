from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from wallet.models import Transaction
from wallet.serializers import TransactionSerializer


class TransactionAPIViewset(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = (IsAuthenticated,)

    #
    # def perform_create(self, serializer):
    #     print(self.request.user)
    #     serializer.save(user=self.request.user)

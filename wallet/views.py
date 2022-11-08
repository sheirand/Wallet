from rest_framework import viewsets
from wallet.models import Transaction
from wallet.serializers import TransactionSerializer


class TransactionAPIViewset(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer



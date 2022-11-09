from rest_framework import serializers
from wallet.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'user', 'amount', 'time', 'category', 'organization', 'description')

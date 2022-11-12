from rest_framework import serializers
from wallet.models import Transaction
from user.serializers import UserSerializer


class TransactionSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(read_only=True)
    user = UserSerializer(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'user', 'amount', 'time', 'category', 'organization', 'description')

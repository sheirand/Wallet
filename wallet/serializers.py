from rest_framework import serializers
from wallet.models import Transaction, Organization, Categories
from user.models import User


class TransactionSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(read_only=True)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)
    organization = serializers.SlugRelatedField(slug_field="title", queryset=Organization.objects.all())
    category = serializers.SlugRelatedField(slug_field="name", queryset=Categories.objects.all())

    class Meta:
        model = Transaction
        fields = ('id', 'user', 'amount', 'time', 'category', 'organization', 'description', 'income')

    def to_internal_value(self, data):
        org_name = data.get("organization")
        Organization.objects.get_or_create(title=org_name)
        return super().to_internal_value(data)

    def create(self, validated_data):
        transaction = validated_data.get("amount")
        income = validated_data.get("income")
        # updating user's balance
        user = User.objects.get(id=self.context["request"].user.id)
        if income:
            user.balance += transaction
        else:
            user.balance -= transaction
        user.save()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # updating user's balance
        user = User.objects.get(id=self.context["request"].user.id)
        new_amount = validated_data.get("amount")

        if instance.income == validated_data.get("income"):
            difference = instance.amount - new_amount
        else:
            difference = instance.amount + new_amount
        user.balance += difference
        user.save()
        return super().update(instance, validated_data)

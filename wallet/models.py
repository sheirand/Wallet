from django.db import models
from user.models import User, Categories


class Organization(models.Model):
    title = models.CharField(verbose_name="Company name", max_length=100)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    user = models.ForeignKey(User, related_name="transactions", on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name="amount", max_digits=15, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories, related_name="transactions", on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, related_name="transactions", on_delete=models.PROTECT)
    description = models.TextField(verbose_name="Transaction description", max_length=400, blank=True, null=True)
    income = models.BooleanField(verbose_name="Income", default=False)

    def __str__(self):
        return str(self.pk)

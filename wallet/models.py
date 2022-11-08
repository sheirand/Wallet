from django.db import models
from user.models import User


class Categories(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    title = models.CharField(verbose_name="Company name", max_length=100)
    location = models.CharField(verbose_name="Company location", max_length=150)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    user = models.ForeignKey(User, related_name="transactions", on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name="amount", max_digits=15, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Categories, blank=True, related_name="transactions")
    organization = models.ForeignKey(Organization, related_name="transactions", on_delete=models.PROTECT)
    description = models.TextField(verbose_name="Transaction description", max_length=400)

from django.contrib.auth.models import AbstractUser
from django.db import models

from user.managers import CustomUserManager


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(verbose_name="email", max_length=150, unique=True)
    balance = models.DecimalField(verbose_name="Balance USD", max_digits=15,
                                  decimal_places=2, default=0.00, blank=True, null=True)
    birthdate = models.DateTimeField(verbose_name="Date of birth", blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    def __str__(self):
        return self.email

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    telephone_number = models.CharField(_("telephone number"), max_length=20, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["telephone_number"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

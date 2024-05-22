from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token


class CustomAccountManager(BaseUserManager):
    """Override Django's default user creation methods to include authentication based on user's email"""

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class AccountType(models.IntegerChoices):
    END_USER = (1, "end_user")
    LIBRARIAN = (2, "librarian")
    ADMIN = (3, "admin")


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=500, unique=True)
    """
    type => Used to define role of account. While checing type of request.user use Account.AccountType to get available types.
    """
    type = models.PositiveSmallIntegerField(
        verbose_name="account_type", choices=AccountType.choices, default=AccountType.END_USER
    )
    phone_num = models.CharField(verbose_name="phone_number", max_length=10, blank=True)
    f_name = models.CharField(verbose_name="first_name", max_length=200, blank=True)
    l_name = models.CharField(verbose_name="last_name", max_length=200, blank=True)

    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = CustomAccountManager()

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None) -> bool:
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_librarian(self) -> bool:
        return self.type == AccountType.LIBRARIAN

    @property
    def is_end_user(self) -> bool:
        return self.type == AccountType.END_USER


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def _create_auth_token(sender: Account, instance: Account, created: bool, **kwargs) -> None:
    """After new Account object is registered, create the corresponding Token for it. This Token object
    is used to authenticate users from REST APIs."""
    if created:
        Token.objects.create(user=instance)

from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name: str, last_name: str, username: str, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Accounts(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128, null=False, default='default_password')
    phone_number = models.CharField(max_length=50)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # trường quyết định khi login
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Các trường yêu cầu khi đk tài khoản (mặc định đã có email), mặc định có password
    
    objects = AccountManager()

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin  # admin có tất cả quyền trong hệ thống

    def has_module_perms(self, add_label):
        return True
    
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"



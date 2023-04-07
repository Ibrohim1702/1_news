from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


# Create your models here.


class ManagerUser(BaseUserManager):
    def create_user(self, phone, password, is_active=True, is_superuser=False, is_staff=False, *args, **kwargs):
        user = self.model(phone=phone,
                          password=password,
                          is_active=is_active,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          **kwargs)
        user.set_password(password)
        return user.save()

    def create_superuser(self, phone, password, **kwargs):
        return self.create_user(phone, password, is_superuser=True, is_staff=True, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=128, null=True, blank=True)
    first_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, null=True, blank=True)
    data_joined = models.DateTimeField(editable=False, auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "phone"
    objects = ManagerUser()
    REQUIRED_FIELDS = ['first_name']

    def format(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.first_name,
            "is_staff": self.is_staff,
            "data_joined": self.data_joined,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
        }


class Otp(models.Model):
    key = models.CharField(max_length=512)
    phone = models.CharField(max_length=20)
    is_expired = models.BooleanField(default=False)
    step = models.CharField(max_length=50)
    tries = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.tries >= 3:
            self.is_expired = True
        return super(Otp, self).save(*args, **kwargs)




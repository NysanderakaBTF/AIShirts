from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have an first name')
        if not last_name:
            raise ValueError('Users must have an last name')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, first_name, last_name, password, **extra_fields)


class DeliveryAddress(models.Model):
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.street_address


class Customer(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    last_login = models.DateTimeField(default=timezone.now)

    #TODO: make delivery address non dublicatable (check before creating)
    delivery_address = models.ManyToManyField(DeliveryAddress, verbose_name="customers", blank=True)

    generation_count = models.SmallIntegerField(default=0)
    daily_limit = models.SmallIntegerField(default=200)
    last_count = models.DateTimeField(null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]

from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
import requests
from decouple import config


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone, password, **extra_fields)


# User model
class User(AbstractBaseUser, PermissionsMixin):

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                 message="Phone number must be entered in the format: '9989012345678'. Up to 14 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    username = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

class Library(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="library")
    image = models.ImageField(upload_to='library_images/', blank=True, null=True)
    address = models.TextField()
    social_media = models.JSONField(blank=True, null=True)  # Masalan, {"telegram": "t.me/library", "instagram": "@library"}
    can_rent_books = models.BooleanField(default=False)

    latitude = models.DecimalField(max_digits=60, decimal_places=50, null=True, blank=True)
    longitude = models.DecimalField(max_digits=60, decimal_places=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.address and (self.latitude is None or self.longitude is None):
            self.get_coordinates()
        super().save(*args, **kwargs)

    def get_coordinates(self):
        """Google Maps API orqali manzil asosida koordinatalarni olish"""
        API_KEY = config("API_KEY")
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": self.address, "key": API_KEY}
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            self.latitude = location["lat"]
            self.longitude = location["lng"]

    def __str__(self):
        return self.user.phone
    
    class Meta:
        verbose_name = 'Library'
        verbose_name_plural = 'Libraries'
    

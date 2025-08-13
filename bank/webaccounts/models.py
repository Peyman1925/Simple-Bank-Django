import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.utils.text import slugify

def get_unique_idcard_filename(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid4().hex}.{ext}"
    return os.path.join('picture/idcard/', unique_filename)

def get_unique_photo_filename(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid4().hex}.{ext}"
    return os.path.join('photo/profile/', unique_filename)


class CustomUser(AbstractUser):
    role_choice = (
        
        ('manager','manager'),
        ('employee','employee'),
        ('user_customer','user_customer'),
        
    )
    
    username = models.CharField(max_length=25, blank=True, null=True, unique=True)
    national_id = models.IntegerField(blank=True, null=True, unique=True)
    picture_for_national_id = models.ImageField(
        upload_to=get_unique_idcard_filename,
        blank = True
    )
    photo = models.ImageField(
        upload_to=get_unique_photo_filename,
        blank = True
    )

    role = models.CharField(choices=role_choice, max_length=20, null=False, blank=False)
    home_address = models.TextField(max_length=300)
    telephone = PhoneNumberField(null=False, blank=False, region="IR")
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone_number = PhoneNumberField(null=False, blank=False, region="IR")
    father_name = models.CharField(max_length=30, null=True, blank=True)
    mother_name = models.CharField(max_length=60, null=True, blank=True)
    account_number = models.CharField(max_length=60, null=True, blank=True)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    register_date = models.DateField(default=timezone.now, blank=False)

    def get_display_name(self):
        
        full_name = f"{self.first_name} {self.last_name}".strip()
        if not full_name:
            full_name = self.username or "user"
        return f"{slugify(full_name)}-{self.id}"

    def __str__(self):
        return str(self.username)

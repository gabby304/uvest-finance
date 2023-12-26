from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _ 
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from typing import List

# Create your models here.

import uuid
from .manager import CustomUserManager


class CustomUser(AbstractUser):
    
    class GenderOptions(models.TextChoices):
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"
    
    username = None 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=GenderOptions.choices)
    phone_number = PhoneNumberField(blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=11, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = CountryField(blank_label=_("Select Country"), null=True, blank=True)  
    last_updated = models.DateTimeField(auto_now=True)
    
    
    USERNAME_FIELD: str = 'email' 
    REQUIRED_FIELDS: List[str] = ["first_name", "last_name"]
    
    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_verified = True 
            self.is_active = True
        return super().save(*args, **kwargs)
        
    @property
    def get_user_fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self) -> str:
        return self.get_user_fullname 
    
    

#models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer' , 'Customer'),
        ('data_entry' , 'Data Entry'),
        ('superuser' , 'Superuser'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    def save(self , *args, **kwargs):
        if self.role in ('data_entry' , 'superuser'):
            self.is_staff = True
        super().save(*args , **kwargs)
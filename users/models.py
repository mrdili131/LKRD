from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=15,unique=True)
    passport_serial = models.CharField(max_length=15,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    balance = models.DecimalField(default=0,max_digits=20,decimal_places=0)
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.passport_serial:
            self.username = self.passport_serial.upper()
        if self.first_name and self.last_name and self.middle_name:
            self.full_name = f'{self.last_name} {self.first_name} {self.middle_name}'
        super().save(*args,**kwargs)

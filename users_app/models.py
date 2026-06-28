import django
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import Group
# Create your models here.
class CustomUser(AbstractUser):
     ROLE_CHOICES = (
         ("ADMIN", "admin"),
         ("MANAGER", "manager"),
         ("EMPLOYEE", "employee"),
     )
     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="EMPLOYEE")
    
    # You can add additional fields here if needed
     phone_number = PhoneNumberField(blank=True, null=True, region="BD")
     def save(self , *args, **kwargs):
        if not self.role:
            self.role = "EMPLOYEE"
        super().save(*args, **kwargs)
        if self.role == "EMPLOYEE":
            group, created = Group.objects.get_or_create(name="EMPLOYEE")
            self.groups.add(group)
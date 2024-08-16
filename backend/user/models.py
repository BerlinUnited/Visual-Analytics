from django.db import models

from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import BaseUserManager



class organization(models.Model):
    name = models.CharField(max_length=100)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Add any additional fields or modifications here
        admin_organization, created = organization.objects.get_or_create(name='admin')
        extra_fields['organization'] = admin_organization

        return self.create_user(email, password, **extra_fields)





class vat_user(AbstractUser):
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    token = models.CharField(max_length=100)
    organization = models.ForeignKey(organization,on_delete=models.SET_NULL,related_name='organizations',blank=True,null=True)
    
    objects = CustomUserManager()

    def __str__(self):
        return self.first_name


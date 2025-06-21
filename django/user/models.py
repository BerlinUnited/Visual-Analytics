from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

class Organization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        Token.objects.create(user=user)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # Add any additional fields or modifications here
        admin_organization, created = Organization.objects.get_or_create(
            name="berlin_united"
        )
        extra_fields["organization"] = admin_organization

        return self.create_user(username, email, password, **extra_fields)


class VATUser(AbstractUser):
    # implicit django behavior: if you inherit from AbstractUser those fields exists by default
    # deactivate them by setting them to None
    first_name = models.CharField(max_length=254, blank=True)
    last_name = models.CharField(max_length=254, blank=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254, blank=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        related_name="organizations",
        blank=True,
        null=True,
    )
    objects = CustomUserManager()

    def __str__(self):
        return self.username

class AllowedEmailDomains(models.Model):
    domain = models.CharField(max_length=100)
    default_organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        related_name="default_orga",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)


class EmailVerificationToken(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_expired(self):
        # Token expires after 24 hours
        return timezone.now() > self.created_at + timezone.timedelta(hours=24)

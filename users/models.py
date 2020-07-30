# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, is_staff: bool, is_superuser: bool, **extra_fields):
        """Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=100)
    picture_url = models.ImageField(null=True)
    name = models.CharField(max_length=255, null=False)
    phone = models.IntegerField(null=True)
    address = models.CharField(max_length=100, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []    
    objects = UserManager()

    def __str__(self):
        return f"{self.email} - {self.name}"

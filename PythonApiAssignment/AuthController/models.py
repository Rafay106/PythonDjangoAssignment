from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

ROLES = (
    ('U', 'User'),
    ('A', 'Admin')
)

class UserModel(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=2551)
    role = models.CharField(max_length=1, choices=ROLES, default='U')
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
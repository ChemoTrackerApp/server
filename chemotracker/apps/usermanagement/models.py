from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

class User (AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    dob = models.DateField(null=True)

    # 0 = not known, 1 = male, 2 = female, 9 = not applicable
    sex = models.PositiveSmallIntegerField()
    date_joined = models.DateTimeField(default=timezone.now)
    phone = models.CharField(max_length=20, null=True)
    address = models.TextField()
    password = models.CharField(maxlength=255)

    def __str__(self):
        return self.email
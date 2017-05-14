from django.db import models

from django.utils import timezone

class User (models.Model):
	first_name = models.CharField()
    last_name = models.CharField()
    age = models.PositiveIntegerField()
    sex = models.PositiveSmallIntegerField()
    date_joined = models.DateTimeField(default=timezone.now)
    
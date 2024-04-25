from django.db import models
from django.contrib.auth.models import User
from .record import Record


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)

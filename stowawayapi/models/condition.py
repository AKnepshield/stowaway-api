from django.db import models


class Condition(models.Model):
    label = models.CharField(max_length=255)

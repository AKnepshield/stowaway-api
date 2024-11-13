from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from stowawayapi.models.condition import Condition


class Record(models.Model):

    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    year_released = models.IntegerField()
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True)
    image_url = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="records")
    genres = models.ManyToManyField(
        "Genre", through="RecordGenre", related_name="records"
    )

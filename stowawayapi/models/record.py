from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from stowawayapi.models.genre import Genre


class Record(models.Model):
    # selected_condition = [
    #     ("POOR", "Poor"),
    #     ("FAIR", "Fair"),
    #     ("GOOD", "Good"),
    #     ("VERY_GOOD", "Very Good"),
    #     ("NEAR_MINT", "Near Mint"),
    # ]
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    year_released = models.IntegerField()
    # selected_condition = models.CharField(max_length=20, choices=selected_condition)
    # genres = models.ManyToManyField(
    #     Genre, through="RecordGenre", related_name="records"
    # )
    # image_url = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="records")

    def clean(self):
        super().clean()
        if not self.genres.exists():
            raise ValidationError("Please choose at least 1 genre")

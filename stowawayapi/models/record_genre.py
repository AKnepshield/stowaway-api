from django.db import models
from .genre import Genre
from .record import Record


class RecordGenre(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

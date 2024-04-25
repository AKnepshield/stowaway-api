from django.db import models
from .record import Record
from .genre import Genre


class RecordGenre(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

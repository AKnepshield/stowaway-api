from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from stowawayapi.models import Record
from stowawayapi.models import Genre
from django.contrib.auth.models import User


class RecordView(ViewSet):

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized instance
        """
        user = request.auth.user

        # genre_ids = request.data.get("genres", [])
        # genres = Genre.objects.filter(pk__in=genre_ids)

        record = Record()
        record.artist = request.data["artist"]
        record.album = request.data["album"]
        record.year_released = request.data["yearReleased"]
        # record.selected_condition = request.data.get("selected_condition")
        # record.image_url = request.data["image_url"]
        record.user = user

        try:
            record.save()
            # record.genres.set(genres)

            serializer = RecordSerializer(record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            record = Record.objects.get(pk=pk)
            record_serializer = RecordSerializer(record)
            record_data = record_serializer.data
            return Response(record_data)

        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET requests for all items
        Returns:
            Response -- JSON serialized array
        """
        try:
            records = Record.objects.all()
            serializer = RecordSerializer(records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class UserRecordSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")

    class Meta:
        model = User
        fields = ("id", "firstName", "lastName", "username")


class RecordGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "label")


class RecordSerializer(serializers.ModelSerializer):
    selected_condition = (
        ("POOR", "Poor"),
        ("FAIR", "Fair"),
        ("GOOD", "Good"),
        ("VERY_GOOD", "Very Good"),
        ("NEAR_MINT", "Near Mint"),
    )
    user = UserRecordSerializer(many=False)
    artist = serializers.CharField()
    album = serializers.CharField()
    yearReleased = serializers.IntegerField(source="year_released")

    class Meta:
        model = Record
        fields = (
            "id",
            "artist",
            "album",
            "yearReleased",
            "user",
        )

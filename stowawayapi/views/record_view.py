from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from stowawayapi.models import Record
from stowawayapi.models import Genre
from stowawayapi.models import Condition
from django.contrib.auth.models import User
from stowawayapi.models.like import Like
from rest_framework.decorators import action


class RecordView(ViewSet):

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized instance
        """
        user = request.auth.user
        condition = Condition.objects.get(pk=request.data["condition"])
        genres = []
        for genre_id in request.data["genres"]:
            genre = Genre.objects.get(pk=genre_id)
            genres.append(genre)

        record = Record()
        record.artist = request.data["artist"]
        record.album = request.data["album"]
        record.year_released = request.data["yearReleased"]
        record.condition = condition
        record.image_url = request.data["imageUrl"]
        record.user = user

        try:
            record.save()
            record.genres.set(genres)

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

    def update(self, request, pk=None):
        try:
            user = request.auth.user
            record = Record.objects.get(pk=pk)
            condition = Condition.objects.get(pk=request.data["condition"])
            genres = []
            for genre_id in request.data["genres"]:
                genre = Genre.objects.get(pk=genre_id)
                genres.append(genre)

            record.artist = request.data["artist"]
            record.album = request.data["album"]
            record.year_released = request.data["yearReleased"]
            record.condition = condition
            record.image_url = request.data["imageUrl"]
            record.user = user
            record.save()
            record.genres.set(genres)

        except Record.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handle GET requests for all items
        Returns:
            Response -- JSON serialized array
        """
        try:
            # Check if a user ID is provided in the query parameters
            user_id = request.query_params.get("user_id")

            if user_id:
                # Filter records by user ID
                records = Record.objects.filter(user_id=user_id)
            else:
                # Retrieve all records
                records = Record.objects.all()
            serializer = RecordSerializer(records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            record = Record.objects.get(pk=pk)
            record.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Record.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=["post", "delete", "get"], detail=True)
    def like(self, request, pk=None):

        user = get_object_or_404(User, user=request.auth.user)
        record = get_object_or_404(Record, pk=pk)

        if request.method == "POST":
            try:
                existing_like = Like.objects.get(record=record, user=user)
                return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            except Like.DoesNotExist:
                like = Like(user=user, record=record)
                like.save()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

        if request.method == "GET":
            existing_like = Like.objects.filter(record=record, user=user).exists()
            return Response({"liked": existing_like}, status=status.HTTP_200_OK)

        elif request.method == "DELETE":
            try:
                like = Like.objects.get(record=record, user=user)
                like.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Like.DoesNotExist:
                return Response(None, status=status.HTTP_404_NOT_FOUND)

    # @action(detail=True, methods=["post", "get", "delete"])
    # def like_record(self, request, pk=None):
    #     record = self.get_object()
    #     user = request.user

    #     if Like.objects.filter(user=user, record=record).exists():
    #         return JsonResponse({"error": "You have already liked this record"})
    #     like = Like.objects.create(user=user, record=record)
    #     return JsonResponse({"message": "Record liked successfully"})


class UserRecordSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")

    class Meta:
        model = User
        fields = ("id", "firstName", "lastName", "username")


class RecordGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class RecordConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ("id", "label")


class RecordSerializer(serializers.ModelSerializer):

    user = UserRecordSerializer(many=False)
    genres = RecordGenreSerializer(many=True)
    condition = RecordConditionSerializer(many=False)
    yearReleased = serializers.IntegerField(source="year_released")
    imageUrl = serializers.CharField(source="image_url")

    class Meta:
        model = Record
        fields = (
            "id",
            "artist",
            "album",
            "yearReleased",
            "imageUrl",
            "condition",
            "genres",
            "user",
        )

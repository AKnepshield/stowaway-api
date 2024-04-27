from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from stowawayapi.models import Condition


class ConditionView(ViewSet):

    def list(self, request):
        """Handle GET requests for all items
        Returns:
            Response -- JSON serialized array
        """
        try:
            conditions = Condition.objects.all()
            serializer = ConditionSerializer(conditions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ("id", "label")

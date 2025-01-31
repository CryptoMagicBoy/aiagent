from rest_framework import serializers

class RequestSerializer(serializers.Serializer):
    query = serializers.CharField(required=True)
    id = serializers.IntegerField(required=True)
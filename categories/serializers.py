from rest_framework import serializers

class CategorySerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50, required=True)
    kind = serializers.CharField(max_length=15, required=True)
    created_at = serializers.DateTimeField(read_only=True)
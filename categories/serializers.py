from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50, required=True, )
    kind = serializers.ChoiceField(choices=Category.CategoryKindChoices.choices, )
    created_at = serializers.DateTimeField(read_only=True, )
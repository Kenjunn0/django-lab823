from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Category
from .serializers import CategorySerializer

@api_view(["GET", "POST"])
def all_categories(request):
    if request.method == "GET":
        serializer = CategorySerializer(Category.objects.all(), many=True)
        return Response({ "Res" : serializer.data })
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ "Res" : serializer.data })


@api_view(["GET", "PUT"])
def category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound

    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response({"Res": serializer.data})
    elif request.method == "PUT":
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({ "Res" : serializer.data })

def create(self, validated_data):
    return Category.objects.create(**validated_data)

def update(self, instance, validated_data):
    instance.name = validated_data.get("name", instance.name)
    instance.kind = validated_data.get("kind", instance.kind)
    instance.save()
    return instance

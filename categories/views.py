from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

@api_view(["GET", "POST"])
def all_categories(request):
    if (request.method == "GET"):
        serializer  = CategorySerializer(Category.objects.all(), many=True)
        return Response({ "Res" : serializer.data })
    elif (request.method == "POST"):
        serializer = CategorySerializer(data=request.data)
        Category.objects.create(name=request.data["name"], kind=request.data["kind"])


@api_view(["GET", "POST"])
def category(request, pk):
    serializer = CategorySerializer(Category.objects.get(pk=pk))
    return Response({ "Res" : serializer.data })
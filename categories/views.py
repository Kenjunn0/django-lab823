from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(ModelViewSet):

    """Category Viewset Definition"""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
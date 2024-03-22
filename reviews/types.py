import strawberry_django
import strawberry
from . import models

@strawberry_django.type(models.Review)
class ReviewType:
    id: strawberry.auto
    payload: strawberry.auto
    rating: strawberry.auto

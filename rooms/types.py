import strawberry
import strawberry_django
from . import models

@strawberry_django.type(models.Room)
class RoomType:
    id: strawberry.auto
    name: strawberry.auto
    kind: strawberry.auto
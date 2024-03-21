import strawberry
import strawberry_django
from . import models

@strawberry_django.type(models.User)
class UserType:
    name: strawberry.auto
    email: strawberry.auto
    username: strawberry.auto
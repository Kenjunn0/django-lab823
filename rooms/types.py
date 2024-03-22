from django.conf import settings
import strawberry
import strawberry_django
from . import models
from users.types import UserType
from reviews.types import ReviewType

@strawberry_django.type(models.Room)
class RoomType:
    id: strawberry.auto
    name: strawberry.auto
    kind: strawberry.auto
    owner: UserType

    @strawberry.field
    def reviews(self, page: int) -> list[ReviewType]:
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        return self.reviews.all()[start:end]

    @strawberry.field
    def rating(self) -> str:
        return self.rating_average()
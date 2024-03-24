import typing
from django.conf import settings
import strawberry
from strawberry.types import Info
import strawberry_django
from . import models
from wishlists.models import Wishlist
from users.types import UserType
from reviews.types import ReviewType


@strawberry_django.type(models.Room)
class RoomType:
    id: strawberry.auto
    name: strawberry.auto
    kind: strawberry.auto
    owner: UserType

    @strawberry.field
    def reviews(self, page: typing.Optional[int] = 1 ) -> list[ReviewType]:
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        return self.reviews.all()[start:end]

    @strawberry.field
    def rating(self) -> str:
        return self.rating_average()

    @strawberry.field
    def is_owner(self, info: Info) -> bool:
        return self.owner == info.context.request.user
    
    @strawberry.field
    def is_liked(self, info: Info) -> bool:
        return Wishlist.objects.filter(
            user=info.context.request.user,
            rooms__pk=self.pk,
        ).exists()


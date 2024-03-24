import typing
import strawberry
from . import types
from .queries import get_all_rooms, get_room
from common.permissions import OnlyLoggedIn


@strawberry.type
class Query:
    get_all_rooms : list[types.RoomType] = strawberry.field(resolver=get_all_rooms, permission_classes=[OnlyLoggedIn], )
    get_room : typing.Optional[types.RoomType] = strawberry.field(resolver=get_room, )
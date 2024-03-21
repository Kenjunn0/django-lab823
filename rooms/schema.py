import strawberry
from . import types
from .queries import get_all_rooms

@strawberry.type
class Query:
    get_all_rooms : list[types.RoomType] = strawberry.field(resolver=get_all_rooms)
import typing
from strawberry.types import Info
from strawberry.permission import BasePermission

class OnlyLoggedIn(BasePermission):

    message = "You need to be logged in"

    def has_permission(self, source: typing.Any, info: Info):
        return info.context.request.user.is_authenticated


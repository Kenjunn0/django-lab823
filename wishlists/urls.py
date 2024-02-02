from django.urls import path
from .views import WishlistDetail, Wishlists, WishlistRoomList

urlpatterns = [
    path("", Wishlists.as_view()),
    path("<int:pk>/", WishlistDetail.as_view()),
    path("<int:pk>/rooms/<int:room_pk>/", WishlistRoomList.as_view())
]

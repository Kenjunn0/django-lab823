from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Room, Amenity
from wishlists.models import Wishlist
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)


    def get_rating(self, room):
        return room.rating_average()

    def get_is_owner(self, room):
        request = self.context["request"]
        return request.user == room.owner

    def get_is_liked(self, room):
        request = self.context["request"]
        if request.user.is_authenticated:
            return Wishlist.objects.filter(user=request.user, rooms__pk = room.pk).exists()
        return False



    class Meta:
        model = Room
        fields = "__all__"


class RoomListSerializer(ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    def get_rating(self, room):
        return room.rating_average()

    def get_is_owner(self, room):
        request = self.context["request"]
        return request.user == room.owner

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos"
        )

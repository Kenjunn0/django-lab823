from django.db import transaction
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from .models import Room, Amenity
from categories.models import Category
from .serializers import RoomListSerializer, RoomDetailSerializer, AmenitySerializer

class Rooms(APIView):

    def get(self, request):
        all_rooms = Room.objects.all()
        return Response(RoomListSerializer(all_rooms, many=True).data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                # category
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("The category's pk not found")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category's kind should be rooms")
                except Category.DoesNotExist:
                    raise ParseError("The category not found")

                try:
                    with transaction.atomic():
                        new_room = serializer.save(owner=request.user, category=category)
                        # amenities
                        amenities = request.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            new_room.amenities.add(amenity)
                        return Response(RoomDetailSerializer(new_room).data)
                except Exception:
                    raise ParseError("Amenity not found")

            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated

class RoomDetail(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        return Response(RoomDetailSerializer(self.get_object(pk)).data)

    def put(self, request, pk):

        room = self.get_object(pk)

        if not request.user.is_authenticated:
            raise NotAuthenticated

        if request.user != room.owner:
            raise PermissionDenied

        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category's kind should be rooms")
                except Category.DoesNotExist:
                    raise ParseError("The category not found")

            try:
                with transaction.atomic():
                    if category_pk:
                        updated_room = serializer.save(category=category)
                    else:
                        updated_room = serializer.save()

                    amenities = request.data.get("amenities")
                    if amenities:
                        updated_room.amenities.clear()
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            updated_room.amenities.add(amenity)
                    return Response(RoomDetailSerializer(updated_room).data)
            except Exception as e:
                print(e)
                raise ParseError("amenity not found")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = Room.objects.get(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Amenities(APIView):
    def get(self, request):
        amenities = Amenity.objects.all()
        serializer = AmenitySerializer(amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            new_amenity = serializer.save()
            return Response(AmenitySerializer(new_amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound


    def get(self, request, pk):
        return Response(
            AmenitySerializer(self.get_object(pk)).data
        )

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from .models import Room, Amenity
from .serializers import RoomListSerializer, RoomDetailSerializer, AmenitySerializer

class Rooms(APIView):

    def get(self, request):
        all_rooms = Room.objects.all()
        return Response(RoomListSerializer(all_rooms, many=True).data)

class RoomDetail(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        return Response(RoomDetailSerializer(self.get_object(pk)).data)


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

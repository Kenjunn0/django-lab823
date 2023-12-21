from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from .models import Room, Amenity
from .serializers import AmenitySerializer


def see_all_rooms(request):
    rooms = Room.objects.all()
    return render(request, "all_rooms.html", {
                      'rooms': rooms,
                      'title': "Hello! this title comes from django!",
                  })

def see_one_room(request, room_id):
  try:
    room = Room.objects.get(pk=room_id)
    return render(request, "room_detail.html",
                  {
                    'room': room,
                  },
                 )
  except Room.DoesNotExist:
    return render(request, "room_detail.html",
                  {
                    "not_found": True,
                  },
                 )

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
        return Response(HTTP_204_NO_CONTENT)

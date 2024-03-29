from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Photo

class PhotoDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if ( photo.room and photo.room.owner != request.user ) or ( photo.experience and photo.experience.host != request.user ):
            return PermissionDenied
        photo.delete()
        return Response(HTTP_204_NO_CONTENT)

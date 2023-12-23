from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from .models import Perk
from .serializers import PerkSerializer

class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        return Response(PerkSerializer(all_perks, many=True).data)

    def post(self, request):
        new_perk = PerkSerializer(data=request.data)
        if new_perk.is_valid():
            return Response(PerkSerializer(new_perk.save()).data)
        else:
            return Response(new_perk.errors)

class PerkDetail(APIView):

    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        return Response(PerkSerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            return Response(serializer.save())
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)

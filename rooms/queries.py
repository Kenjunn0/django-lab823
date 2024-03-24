import strawberry
from .models import Room

def get_all_rooms():
    return Room.objects.all()

def get_room(pk:int):
    try:
        return Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return None
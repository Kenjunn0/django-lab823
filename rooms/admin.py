from django.contrib import admin
from .models import Room, Amenity


@admin.action(description="Make rooms pet-friendly")
def make_rooms_pet_friendly(modeladmin, request, queryset):
    queryset.update(pet_friendly=True)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = [make_rooms_pet_friendly, ]

    list_display = (
        "name",
        "price",
        "kind",
        "owner",
        "rating_average",
        "total_amenities",
        "created_at",
    )

    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
        "price"
    )

    def total_amenities(self, obj):
        return obj.amenities.count()


@admin.register(Amenity)
class Amenity(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
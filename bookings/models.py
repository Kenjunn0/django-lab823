from django.db import models
from common.models import CommonModel

class Booking(CommonModel):

    """Booking model Definition"""

    class BookingKindChoices(models.TextChoices):
        ROOM = "room", "Room"
        EXPERIENCE = "experience", "Experience"

    kind = models.CharField(max_length=15, choices=BookingKindChoices.choices, )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, )
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, null=True, blank=True, )
    experience = models.ForeignKey("experiences.Experience", on_delete=models.CASCADE, null=True, blank=True, )
    check_in = models.DateField()
    check_out = models.DateField()
    experience_time = models.DateTimeField(null=True, blank=True, )
    guest = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.kind} : {self.user}"
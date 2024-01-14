from django.db import models
from common.models import CommonModel

class Photo(CommonModel):

    """Photo for Media Definition"""

    file = models.URLField()
    description = models.CharField(max_length=140, blank=True, )
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, null=True, blank=True, related_name="photos", )
    experience = models.ForeignKey("experiences.Experience", on_delete=models.CASCADE, null=True, blank=True, related_name="photos", )

    def __str__(self):
        return "Photo file"

class Video(CommonModel):

    """Video for Media Definition"""

    file = models.URLField()
    experience = models.OneToOneField("experiences.Experience", on_delete=models.CASCADE, related_name="video", )

    def __str__(self):
        return "Video file"





from django.db import models
from common.models import CommonModel

class Photo(CommonModel):

    """Photo for Media Definition"""

    file = models.ImageField(upload_to="medias", )
    description = models.CharField(max_length=140, blank=True, )
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, null=True, blank=True, )
    experience = models.ForeignKey("experiences.Experience", on_delete=models.CASCADE, null=True, blank=True, )

    def __str__(self):
        return "Photo file"

class Video(CommonModel):

    """Video for Media Definition"""

    file = models.FileField()
    experience = models.OneToOneField("experiences.Experience", on_delete=models.CASCADE, )

    def __str__(self):
        return "Video file"





from django.db import models
from common.models import CommonModel
class Category(CommonModel):

    """Rooms or Experience Category Model Definition"""

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    class CategoryKindChoices(models.TextChoices):
        ROOMS = "rooms", "Rooms"
        EXPERIENCES = "experiences", "Experiences"

    name = models.CharField(max_length=50, )
    kind = models.CharField(max_length=15, choices=CategoryKindChoices.choices, )

    def __str__(self):
        return f"{self.kind.title()} : {self.name}"

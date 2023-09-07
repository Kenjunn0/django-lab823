from django.db import models
from common.models import CommonModel


class Experience(CommonModel):
    """Experience Model Definition"""

    name = models.CharField(max_length=180, default="")
    country = models.CharField(max_length=50, default="The Republic of Korea")
    city = models.CharField(max_length=80, default="Seoul")
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField("experiences.Perk", )
    categories = models.ForeignKey("categories.Category", on_delete=models.SET_NULL, null=True, blank=True, )

    def __str__(self):
        return self.name


class Perk(CommonModel):
    """what is included on the experience"""

    name = models.CharField(max_length=80, blank=True, default="", )
    detail = models.CharField(max_length=140, blank=True, default="", )
    explanation = models.TextField()

    def __str__(self):
        return self.name

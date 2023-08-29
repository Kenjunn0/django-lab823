from django.db import models

class House(models.Model):
    """Model Definition for House"""

    name = models.CharField(max_length=140)
    price_per_night = models.PositiveIntegerField(verbose_name="Price")
    description = models.TextField()
    address = models.CharField(max_length=140)
    pets_allowed = models.BooleanField(default=True, verbose_name="Pets", help_text="Does That House Allow Pets to Come")

    def __str__(self):
        return self.name
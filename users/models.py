from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "FEMALE")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        # 소괄호 없이 작성해도 Tuple로 인식할 수 있다.
        KRW = "krw", "Korea, KRW"
        USD = "usd", "USA, USD"

    first_name = models.CharField(max_length=150, editable=False, )
    last_name = models.CharField(max_length=150, editable=False, )
    name = models.CharField(max_length=150, default="")
    profile_photo = models.URLField(blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, )
    is_host = models.BooleanField(default=False)
    language = models.CharField(max_length=2, choices=LanguageChoices.choices, )
    currency = models.CharField(max_length=5, choices=CurrencyChoices.choices, )

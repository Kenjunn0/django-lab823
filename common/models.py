from django.db import models

class CommonModel(models.Model):

    """Common Model Definition"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # abstract = True 는 데이터베이스에 등록되지 않는다.

    class Meta:
        abstract = True
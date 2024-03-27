# 사용하지 않음
# from django.test import TestCase
from rest_framework.test import APITestCase
from . import models

class TestAmenities(APITestCase):

    NAME = "Amenities Name"
    DESCRIPTION = "Amenities Description"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION
        )

    def test_all_amenities(self):
        response = self.client.get("/api/v1/rooms/amenities")
        data = response.json()
        self.assertEquals(response.status_code, 200, "status_code isn't 200")
        self.assertIsInstance(data, list, )
        self.assertEquals(len(data), 1, )
        self.assertEquals(data[0]['name'], self.NAME, )
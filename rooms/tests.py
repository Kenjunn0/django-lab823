# 사용하지 않음
# from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from . import models
from users.models import User

class TestAmenities(APITestCase):

    NAME = "Amenities Name"
    DESCRIPTION = "Amenities Description"
    URL = "/api/v1/rooms/amenities"

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION
        )

    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()
        self.assertEquals(response.status_code, 200, "status_code isn't 200")
        self.assertIsInstance(data, list, )
        self.assertEquals(len(data), 1, )
        self.assertEquals(data[0]['name'], self.NAME, )

    def test_create_amenity(self):

        new_amenity = "new_amenity"
        new_amenity_desc = "new_amenity_desc"

        # 정상 요청 테스트
        response = self.client.post(self.URL, data={
            "name": new_amenity,
            "description": new_amenity_desc,
        })
        data = response.json()

        self.assertEquals(response.status_code, 200, "status_code isn't 200, It should be 200")
        self.assertEquals(data["name"], new_amenity, "data[\"name\"] is not matched up with the input data")
        self.assertEquals(data["description"], new_amenity_desc, "data[\"description\"] is not matched up with the input data")

        # 데이터 누락 시 요청 테스트
        response = self.client.post(self.URL, data= {})
        data = response.json()

        self.assertEquals(response.status_code, 400, "status_code isn't 400, It should be 400")
        self.assertIn("name", data)


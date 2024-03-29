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


class TestAmenity(APITestCase):

    NAME = "Test Amenity"
    DESCRIPTION = "Test Dsc"
    URL = "/api/v1/rooms/amenities"

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION
        )

    def test_amenity_not_found(self):
        response = self.client.get(f"{self.URL}/2")
        self.assertEquals(response.status_code, 404)

    def test_get_amenity(self):
        response = self.client.get(f"{self.URL}/1")
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data["name"], self.NAME)
        self.assertEquals(data["description"], self.DESCRIPTION)


    def test_put_amenity(self):
        pass

    def test_delete_amenity(self):
        response = self.client.delete(f"{self.URL}/1")
        self.assertEquals(response.status_code, 204)

class TestRooms(APITestCase):

    URL = "/api/v1/rooms/"

    def setUp(self):
        user = User.objects.create(
            username="test"
        )
        user.set_password("123")
        user.save()
        self.user = user

    def test_create_room(self):

        response = self.client.post(self.URL)
        self.assertEquals(response.status_code, 403)

        # self.client.login(username="test", password="123",)
        self.client.force_login(self.user)

        response = self.client.post(self.URL)
        self.assertEquals(response.status_code, 400)
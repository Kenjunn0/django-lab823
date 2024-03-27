# 사용하지 않음
# from django.test import TestCase
from rest_framework.test import APITestCase

class TestAmenities(APITestCase):

    def test_two_plus_two(self):
        self.assertEquals(2+2, 4, "there is a mistake")
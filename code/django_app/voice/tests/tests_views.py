from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class TestVoiceCreateAPIView(APITestCase):
    TARGET_IRL = "/api"

from django.test import TestCase

from django.contrib.auth.models import User
from .models import Main_food, Profile_user, Daily_food

# Create your tests here.
class TestModels(TestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

    def test_profile_added(self):
        profiles = Profile_user.objects.all().count()
        self.assertEqual(profiles, 2)
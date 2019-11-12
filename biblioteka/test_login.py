from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.db.utils import IntegrityError
from django.urls import reverse

from biblioteka.models import Author, Book, Library
from biblioteka.utils import *
            

class LoginTestCase(TestCase):
    def setUp(self):
        self.username = "test"
        self.password = 'pass@123#'
        self.email = "test@test.com"
        self.user = User.objects.create(username=self.username, password=self.password, email=self.email)
        self.client = Client()

    def test_profile_view_with_logged_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('biblioteka:profile'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_view_without_logged_user(self):
        response = self.client.get('/profile/', follow=False)
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/profile/', follow=True)
        self.assertEqual(len(response.redirect_chain), 1)

from django.test import TestCase
from django.test.client import Client
from mainapp.models import Post, Category
from django.core.management import call_command


class TestMainappSmoke(TestCase):
    fixtures = ['mainapp.json']

    # def setUp(self):
    #      call_command('flush', '--noinput')
    #      self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/help/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/category/dizajn/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/post/nazvanie/')
        self.assertEqual(response.status_code, 200)

    # def tearDown(self):
    #     call_command('sqlsequencereset', 'mainapp', 'authapp', 'blogapp')

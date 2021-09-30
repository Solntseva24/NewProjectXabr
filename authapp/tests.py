from django.test import TestCase
from django.test.client import Client
from authapp.models import XabrUser


class TestUserManagement(TestCase):
    fixtures = ['authapp.json', 'mainapp.json']

    def setUp(self):
        # call_command('flush', '--noinput')
        # # call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.superuser = XabrUser.objects.create_superuser('django2', \
                                                           'django2@xabr.local', 'geekbrains')

        self.user = XabrUser.objects.create_user('tarantino', \
                                                 'tarantino@xabr.local', 'geekbrains')

        self.user_with__first_name = XabrUser.objects.create_user('umaturman', \
                                                                  'umaturman@xabr.local', 'geekbrains',
                                                                  first_name='Ума')

    def test_user_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['page_title'], 'главная')
        self.assertNotContains(response, 'Пользователь', status_code=200)

        # данные пользователя
        self.client.login(username='tarantino', password='geekbrains')

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        # главная после логина
        response = self.client.get('/')
        self.assertContains(response, 'Пользователь', status_code=200)
        self.assertEqual(response.context['user'], self.user)

        # self.assertIn('Пользователь', response.content.decode())

    def test_user_logout(self):
        # данные пользователя
        self.client.login(username='tarantino', password='geekbrains')

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        # выходим из системы
        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)

        # главная после выхода
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_user_register(self):
        # логин без данных пользователя
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'регистрация')
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'samuel',
            'first_name': 'Сэмюэл',
            'last_name': 'Джексон',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'sumuel@shop.local',
            'age': '21'
        }

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = XabrUser.objects.get(username=new_user_data['username'])
        self.assertTrue(new_user.is_active)

        # данные нового пользователя
        self.client.login(
            username=new_user_data['username'],
            password=new_user_data['password1']
        )

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        # проверяем главную страницу
        response = self.client.get('/')
        self.assertContains(response, text=new_user_data['first_name'], status_code=200)

    # def tearDown(self):
    #     call_command('sqlsequencereset', 'mainapp', 'authapp', 'blogapp')

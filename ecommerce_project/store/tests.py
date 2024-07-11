from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationTests(TestCase):
    
    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/register.html')

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'Testpass123',
            'password2': 'Testpass123'
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, reverse('login'))

    def test_login_view(self):
        User.objects.create_user(username='testuser', password='Testpass123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'Testpass123'
        })
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('home'))

    def test_logout_view(self):
        User.objects.create_user(username='testuser', password='Testpass123')
        self.client.login(username='testuser', password='Testpass123')
        response = self.client.post(reverse('logout'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('home'))

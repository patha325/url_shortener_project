from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import URL

class URLShortenerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_url_creation(self):
        response = self.client.post('/create/', {'original_url': 'http://example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(URL.objects.filter(user=self.user).exists())

    def test_url_shortening_creation(self):
        url = URL.objects.create(
            user=self.user,
            original_url="http://example.com",
            short_url="abc123"
        )
        self.assertEqual(url.original_url, "http://example.com")
        self.assertEqual(url.short_url, "abc123")
        self.assertEqual(url.user, self.user)
        self.assertEqual(url.clicks, 0)  # Default should be 0

    def test_url_string_representation(self):
        url = URL.objects.create(
            user=self.user,
            original_url="http://example.com",
            short_url="abc123"
        )
        self.assertEqual(str(url), "abc123")

    def test_url_redirection(self):
        url = URL.objects.create(user=self.user, original_url='http://example.com', short_url='abc123')
        response = self.client.get('/abc123/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://example.com')

    def test_url_list_view(self):
        response = self.client.get(reverse('url-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'url_list.html')

    def test_url_create_view_get(self):
        response = self.client.get(reverse('url-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'url_create.html')

    def test_url_create_view_post(self):
        data = {'original_url': 'http://example.com'}
        response = self.client.post(reverse('url-create'), data)
        self.assertEqual(response.status_code, 302)  # Redirects after creation
        self.assertTrue(URL.objects.filter(original_url='http://example.com').exists())
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Tag

User = get_user_model()

class CategoryAPITestCase(APITestCase):

    def setUp(self):
        # Create regular user and superuser
        self.user = User.objects.create_user(username='user', password='testpassword')
        self.superuser = User.objects.create_superuser(username='superuser', password='superpassword')

        # Create tokens for auth
        self.user_token = Token.objects.create(user=self.user)
        self.superuser_token = Token.objects.create(user=self.superuser)

        # API URL
        self.url = reverse('category-list')

        # Categories to test
        self.public_cat = Category.objects.create(user=self.superuser, name='Public Cat', is_public=True)
        self.private_cat = Category.objects.create(user=self.user, name='Private Cat', is_public=False)
        self.private_cat2 = Category.objects.create(user=self.superuser, name='Private Cat 2', is_public=False)

    def test_list_categories_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Regular user should see their own private category and the public category
        self.assertEqual(len(response.data), 2)
        self.assertIn(self.public_cat.name, [c['name'] for c in response.data])
        self.assertIn(self.private_cat.name, [c['name'] for c in response.data])
        self.assertNotIn(self.private_cat2.name, [c['name'] for c in response.data])

    def test_list_categories_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token.key}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Superuser should see all categories
        self.assertEqual(len(response.data), 3)

    def test_create_private_category_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        data = {'name': 'New Private Cat', 'is_public': True} # User tries to create a public category
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.data['is_public']) # The backend should have forced is_public to False

    def test_create_public_category_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token.key}')
        data = {'name': 'Superuser Public Cat', 'is_public': True}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['is_public'])

    def test_unauthenticated_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)


class TagAPITestCase(APITestCase):

    def setUp(self):
       # Create regular user and superuser
        self.user = User.objects.create_user(username='user', password='testpassword')
        self.superuser = User.objects.create_superuser(username='superuser', password='superpassword')

        self.user_token = Token.objects.create(user=self.user)
        self.superuser_token = Token.objects.create(user=self.superuser)

        self.url = reverse('tag-list')

        self.public_tag = Tag.objects.create(user=self.superuser, name='public-tag', is_public=True)
        self.private_tag = Tag.objects.create(user=self.user, name='private-tag', is_public=False)
        self.private_tag2 = Tag.objects.create(user=self.superuser, name='private-tag2', is_public=False)

    def test_list_tags_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(self.public_tag.name, [t['name'] for t in response.data])
        self.assertIn(self.private_tag.name, [t['name'] for t in response.data])
        self.assertNotIn(self.private_tag2.name, [t['name'] for t in response.data])

    def test_list_tags_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token.key}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_create_private_tag_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        data = {'name': 'new-private-tag', 'is_public': True}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.data['is_public'])

    def test_create_public_tag_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token.key}')
        data = {'name': 'superuser-public-tag', 'is_public': True}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['is_public'])

    def test_unauthenticated_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
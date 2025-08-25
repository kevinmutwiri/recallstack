from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Flashcard, Tag

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


class FlashcardAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='testpassword')
        self.superuser = User.objects.create_superuser(username='superuser', password='superpassword')

        self.user_token = Token.objects.create(user=self.user)
        self.superuser_token = Token.objects.create(user=self.superuser)

        self.url = reverse('flashcard-list')

        # Create public category and tags
        self.public_category = Category.objects.create(user=self.superuser, name='Public Cat', is_public=True)
        self.public_tag1 = Tag.objects.create(user=self.superuser, name='public-tag-1', is_public=True)
        self.public_tag2 = Tag.objects.create(user=self.superuser, name='public-tag-2', is_public=True)

        # Create private category and tags for the regular user
        self.private_category = Category.objects.create(user=self.user, name='My Private Cat', is_public=False)
        self.private_tag = Tag.objects.create(user=self.user, name='private-tag-1', is_public=False)

        # Create flashcards for testing
        self.public_flashcard_code = Flashcard.objects.create(
            user=self.superuser,
            question="What is a binary search tree?",
            answer="A data structure...",
            category=self.public_category,
            is_code_snippet=True,
            is_public=True
        )
        self.public_flashcard_code.tags.set([self.public_tag1, self.public_tag2])

        self.private_flashcard_code = Flashcard.objects.create(
            user=self.user,
            question="What is a Python decorator?",
            answer="A function that takes another function...",
            category=self.private_category,
            is_code_snippet=True,
            is_public=False
        )
        self.private_flashcard_code.tags.set([self.private_tag])

        self.private_flashcard2 = Flashcard.objects.create(
            user=self.superuser,
            question="Private question by superuser",
            answer="Private answer",
            category=self.private_category,
            is_code_snippet=False,
            is_public=False
        )

    def test_list_flashcards_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Regular user should only see their own private flashcard and the public one
        self.assertEqual(len(response.data), 2)
        self.assertIn(self.public_flashcard_code.question, [f['question'] for f in response.data])
        self.assertIn(self.private_flashcard_code.question, [f['question'] for f in response.data])
        self.assertNotIn(self.private_flashcard2.question, [f['question'] for f in response.data])

    def test_create_flashcard_with_public_content_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token.key}')
        data = {
            "question": "Superuser public flashcard",
            "answer": "Answer",
            "category": self.public_category.id,
            "tags": [self.public_tag1.id],
            "is_public": True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['is_public'])

    def test_create_flashcard_as_authenticated_user_always_sets_is_public_to_false(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        data = {
            "question": "User private flashcard",
            "answer": "Answer",
            "category": self.public_category.id, # Use a public category
            "tags": [self.public_tag1.id],      # Use a public tag
            "is_public": True  # Attempt to create public content
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        # The backend should have forced is_public to false
        self.assertFalse(response.data['is_public'])

    def test_create_public_flashcard_with_private_category_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token.key}')
        data = {
            "question": "Public flashcard with private category",
            "answer": "Answer",
            "category": self.private_category.id, # Link to a private category
            "tags": [self.public_tag1.id],
            "is_public": True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('category', response.data)

    def test_create_public_flashcard_with_private_tag_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token.key}')
        data = {
            "question": "Public flashcard with private tag",
            "answer": "Answer",
            "category": self.public_category.id,
            "tags": [self.private_tag.id], # Link to a private tag
            "is_public": True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('tags', response.data)
    
    def test_flashcard_list_can_be_filtered_by_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.get(f'{self.url}?category_id={self.private_category.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question'], self.private_flashcard_code.question)

    def test_flashcard_list_can_be_filtered_by_tags(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        tag_ids = f'{self.public_tag1.id},{self.public_tag2.id}'
        response = self.client.get(f'{self.url}?tag_ids={tag_ids}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question'], self.public_flashcard_code.question)

    def test_flashcard_list_can_be_filtered_by_is_code_snippet(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.get(f'{self.url}?is_code_snippet=true')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        
    def test_unauthenticated_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
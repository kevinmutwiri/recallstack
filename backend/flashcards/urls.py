from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, FlashcardViewSet, TagViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'flashcards', FlashcardViewSet, basename='flashcard')

urlpatterns = [
    path('', include(router.urls)),
]
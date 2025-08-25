from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from .models import Category, Flashcard, Tag
from .serializers import CategorySerializer, FlashcardSerializer, TagSerializer
from django.db.models import Q

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Superusers can see all categories. Regular users see their own + public ones.
        if user.is_superuser:
            return Category.objects.all()
        return Category.objects.filter(Q(user=user) | Q(is_public=True))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Superusers can see all tags. Regular users see their own and all public ones.
        if user.is_superuser:
            return Tag.objects.all()
        return Tag.objects.filter(Q(user=user) | Q(is_public=True))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FlashcardViewSet(viewsets.ModelViewSet):
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['question', 'answer']

    def get_queryset(self):
        user = self.request.user
        queryset = Flashcard.objects.all()

        # A superuser can see all flashcards.
        if not user.is_superuser:
            # Regular users can only see their own flashcards OR public ones.
            queryset = queryset.filter(Q(user=user) | Q(is_public=True))

        # Filtering logic based on query parameters
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        
        tag_ids = self.request.query_params.get('tag_ids')
        if tag_ids:
            tag_list = tag_ids.split(',')
            queryset = queryset.filter(tags__id__in=tag_list)

        is_code_snippet = self.request.query_params.get('is_code_snippet')
        if is_code_snippet is not None:
            queryset = queryset.filter(is_code_snippet=is_code_snippet.lower() == 'true')

        return queryset.distinct()

    def perform_create(self, serializer):
        # Regular users can only create private flashcards
        if not self.request.user.is_superuser:
            serializer.validated_data['is_public'] = False
        serializer.save(user=self.request.user)
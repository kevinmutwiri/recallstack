from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, Tag
from .serializers import CategorySerializer, TagSerializer
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
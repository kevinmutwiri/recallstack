from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .serializers import CategorySerializer
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
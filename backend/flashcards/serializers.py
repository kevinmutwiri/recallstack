from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'short_name', 'parent', 'description', 'is_public']
        read_only_fields = ['user']

    def create(self, validated_data):
        # Enforce that regular users can only create private categories
        if not self.context['request'].user.is_superuser:
            validated_data['is_public'] = False
        return super().create(validated_data)
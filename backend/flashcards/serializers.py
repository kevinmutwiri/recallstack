from rest_framework import serializers
from .models import Category, Flashcard, Tag

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
    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'user', 'name', 'is_public']
        read_only_fields = ['user']

    def create(self, validated_data):
        # A regular user can only create private tags.
        if not self.context['request'].user.is_superuser:
            validated_data['is_public'] = False
        return super().create(validated_data)
    

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = [
            'id', 'user', 'question', 'answer', 'category', 'tags',
            'is_code_snippet', 'is_public', 'ease_factor', 'repetitions',
            'interval', 'last_reviewed', 'next_review_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'ease_factor', 'repetitions', 'interval', 'last_reviewed', 'next_review_date']

    def validate(self, data):
        if data.get('is_public', False):
            # Check if associated category is public
            category = data.get('category')
            if category and not category.is_public:
                raise serializers.ValidationError({"category": "Public flashcards must be linked to a public category."})

            # Check if all associated tags are public
            tags = data.get('tags')
            if tags and any(not tag.is_public for tag in tags):
                raise serializers.ValidationError({"tags": "Public flashcards must be linked to public tags only."})

        return data
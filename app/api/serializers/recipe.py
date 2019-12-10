from rest_framework import serializers
from api.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a Recipe"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)

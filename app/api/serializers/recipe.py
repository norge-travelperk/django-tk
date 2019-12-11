from rest_framework import serializers
from api.models import Recipe, Ingredient
from api.serializers.ingredient import IngredientSerializer


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a Recipe"""

    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)

        for attr, value in validated_data.items():
            if value:
                setattr(instance, attr, value)

        if ingredients_data:
            instance.ingredients.all().delete()
            for ingredient_data in ingredients_data:
                Ingredient.objects.create(recipe=instance, **ingredient_data)

        instance.save()
        instance.refresh_from_db()
        return instance

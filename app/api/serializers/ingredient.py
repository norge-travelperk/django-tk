from rest_framework import serializers
from api.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('name', )
        read_only_fields = ('id',)

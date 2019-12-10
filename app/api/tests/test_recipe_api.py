from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from api.models import Recipe
from api.serializers import RecipeSerializer

RECIPES_URL = reverse("api:recipe-list")


def sample_recipe(**params):
    """Creates and returns a sample recipe"""

    default = {
        'name': 'Sample name',
        'description': 'Sample Description'
    }
    default.update(params)
    return Recipe.objects.create(**default)


class RecipeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipe(self):
        sample_recipe(name="Cheese")
        sample_recipe(name="Pasta")

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

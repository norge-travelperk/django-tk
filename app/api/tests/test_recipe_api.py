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


def detail_url(recipe_id):
    return reverse('api:recipe-detail', args=[recipe_id])


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

    def test_create_basic_recipe(self):
        """Test creating a recipe"""
        payload = {
            'name': 'Cheese',
            'description': 'Test Description'
        }
        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_view_recipe_detail(self):
        recipe = sample_recipe()
        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_delete_recipe(self):
        recipe = sample_recipe()
        url = detail_url(recipe.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        exist = Recipe.objects.filter(id=recipe.id)
        self.assertFalse(exist)

    # TODO: test_update_recipe(self):
    # TODO: test_add_ingredients(self):
    # TODO: test_remove_ingredients(self):

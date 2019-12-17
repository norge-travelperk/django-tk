from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework.test import APIClient
from rest_framework import status

from api.models import Recipe, Ingredient
from api.serializers import RecipeSerializer
import json

RECIPES_URL = reverse("api:recipe-list")


def sample_recipe(**params):
    """Creates and returns a sample recipe"""

    default = {
        'name': 'Sample name',
        'description': 'Sample Description'
    }
    default.update(params)
    return Recipe.objects.create(**default)


def sample_ingredient(name="Sample Ingredient"):
    return Ingredient(name=name)


def detail_url(recipe_id):
    return reverse('api:recipe-detail', args=[recipe_id])


def list_url_params(**kwargs):
    if kwargs:
        return '{}?{}'.format(RECIPES_URL, urlencode(kwargs))
    return RECIPES_URL


class RecipeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipe(self):
        sample_recipe(name="Cheese")
        sample_recipe(name="Pasta")
        sample_recipe(name="Frijoles")
        sample_recipe(name="Costa")

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 4)

    def test_create_basic_recipe(self):
        """Test creating a recipe"""
        payload = {
            'name': 'Pasta',
            'description': 'Worm it up a bit',
            'ingredients': [
                    {'name': 'dough'},
                    {'name': 'cheese'},
                    {'name': 'tomato'},
            ],
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])
        self.assertEqual(len(ingredients), 3)
        for i in range(3):
            self.assertEqual(ingredients[i].name, payload.ingredients[i])

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

    def test_filter_recipes_by_name(self):
        sample_recipe(name="Cheese")
        sample_recipe(name="Pasta")
        sample_recipe(name="Mustard")
        res = self.client.get(list_url_params(name="a"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        for value in res.data:
            self.assertTrue("a" in value['name'])

    def test_patch_name_on_recipes(self):
        recipe = sample_recipe(name="Cheese")
        url = detail_url(recipe.id)
        payload = {
            'name': 'Pasta'
        }
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])

    def test_patch_ingredients_on_recipes(self):
        recipe = sample_recipe(name="Cheese")
        recipe.ingredients.create(name="a")
        recipe.ingredients.create(name="b")
        recipe.ingredients.create(name="c")

        url = detail_url(recipe.id)
        payload = {
            'ingredients': [
                {'name': 'dough'},
                {'name': 'cheese'},
            ],
        }
        res = self.client.patch(url, json.dumps(
            payload), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()
        self.assertEqual(len(recipe.ingredients.all()), 2)

    # TODO: test_add_ingredients(self):
    # TODO: test_remove_ingredients(self):

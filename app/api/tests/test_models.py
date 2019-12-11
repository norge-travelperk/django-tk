from django.test import TestCase

from api.models import Recipe, Ingredient


def sample_recipe(**params):
    """Creates and returns a sample recipe"""

    default = {
        'name': 'Sample name',
        'description': 'Sample Description'
    }
    default.update(params)
    return Recipe.objects.create(**default)


class ModelTest(TestCase):

    def test_recipe_str(self):
        recipe = Recipe.objects.create(
            name="Pizza",
            description="Put it in the oven"
        )
        self.assertEqual(str(recipe), recipe.name)

    def test_ingredient_str(self):
        ingredient = Ingredient.objects.create(
            name="Pepper",
            recipe=sample_recipe()
        )
        self.assertEqual(str(ingredient), ingredient.name)

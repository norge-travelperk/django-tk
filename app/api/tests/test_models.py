from django.test import TestCase

from api.models.recipe import Recipe


class ModelTest(TestCase):

    def test_recipe_str(self):
        recipe = Recipe.objects.create(
            name="Pizza",
            description="Put it in the oven"
        )
        self.assertEqual(str(recipe), recipe.name)

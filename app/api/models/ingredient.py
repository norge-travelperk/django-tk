from django.db import models
from api.models import Recipe


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

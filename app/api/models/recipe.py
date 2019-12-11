from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField(
        max_length=1000, blank=True)  # TODO: allow blank

    def __str__(self):
        return self.name

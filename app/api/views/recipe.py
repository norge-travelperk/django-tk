from rest_framework import viewsets
from api.serializers import RecipeSerializer
from api.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset.order_by('-id')

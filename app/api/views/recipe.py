from rest_framework import viewsets
from api.serializers import RecipeSerializer
from api.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        name_filter = self.request.query_params.get('name', None)
        if name_filter:
            queryset = queryset.filter(name__contains=name_filter)
        return queryset

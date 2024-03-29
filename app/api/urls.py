from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet


router = DefaultRouter()
router.register('recipes', RecipeViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls))
]

from django.urls import path
from .views import *
from .utils import get_nutrition_data

urlpatterns = [
    path('', Home, name='main-home' ),
    path('tdee/', TdeePage.as_view(), name='main-tdee' ),
    path('nutrition/', NutritionPage.as_view(), name='main-nutrition' ),
    path('api/get-nutrition-data/', get_nutrition_data, name='main-get_nutrition_data'),
]
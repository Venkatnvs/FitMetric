from django.urls import path
from .views import *
from .utils import get_nutrition_data,save_nutrition_data,delete_nutrition_data

urlpatterns = [
    path('', Home, name='main-home' ),
    path('tdee/', TdeePage.as_view(), name='main-tdee' ),
    path('nutrition/', NutritionPage.as_view(), name='main-nutrition' ),
    path('mental-health/', MentalHealthPage.as_view(), name='main-mental-health' ),
    path('api/get-nutrition-data/', get_nutrition_data, name='main-get_nutrition_data'),
    path('api/save_nutrition_data/', save_nutrition_data, name='main-save_nutrition_data'),
    path('api/delete_nutrition_data/<int:item_id>/', delete_nutrition_data, name='main-delete_nutrition_data'),
]
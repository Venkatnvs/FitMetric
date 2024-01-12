from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='games-home' ),
    path('color-game', ColorGames.as_view(), name='games-color-game' ),
]
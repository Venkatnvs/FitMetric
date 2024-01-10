from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='predict-home' ),
    path('mental-health', MentalHealthPage.as_view(), name='predict-mental-health' ),
]
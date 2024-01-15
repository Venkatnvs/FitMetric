from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='predict-home' ),
    path('depression-level', DepressionLevelPage.as_view(), name='predict-depression-level' ),
    path('diabetes', DiabetesPredict.as_view(), name='predict-diabetes' ),
    path('heart', HeartPrediction.as_view(), name='predict-heart' ),
    path('breast-cancer', BreastCancerPredict.as_view(), name='predict-breast-cancer' ),
    path('liver', LiverPredict.as_view(), name='predict-liver' ),
    path('kidney', KidneyPredict.as_view(), name='predict-kidney' ),
    path('diseases', DiseasesPredict.as_view(), name='predict-diseases' ),
]
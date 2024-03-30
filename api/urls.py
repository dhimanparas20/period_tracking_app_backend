from django.urls import path,include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'user', PeriodViewSet, basename='period')

urlpatterns = [
    path('',include(router.urls)),   # for above routers
    path('login/', Login.as_view(), name="login"),
    path('calculate_average_cycle_length/', PeriodViewSet.as_view({'get': 'calculate_average_cycle_length'}), name='calculate-average-cycle-length'),
    path('predict_next_period/', PeriodViewSet.as_view({'get': 'predict_next_period'}), name='predict_next_period'),
    path('analyze_symptoms_count/', PeriodViewSet.as_view({'get': 'analyze_symptoms_count'}), name='analyze_symptoms_count'),
    
]

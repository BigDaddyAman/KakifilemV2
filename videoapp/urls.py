from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('countdown/', views.countdown, name='countdown'),
    path('health/', views.health_check, name='health_check'),  # Add this line
]

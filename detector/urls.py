from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detect/', views.detect_fingers, name='detect'),
]
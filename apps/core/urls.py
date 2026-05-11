from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vibe/', views.vibe_check, name='vibe_check'),
]
from django.urls import path, reverse
from . import views

urlpatterns = [
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('api/scores/', views.record_score, name='record_score'),
]



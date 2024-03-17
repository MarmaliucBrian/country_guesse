from django.urls import path
from .views import MapGameView, HomeView, CheckGuessView

urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),  # URL for the home page
    path('map-game/', MapGameView.as_view(), name='map_game'),  # URL for the map game page
    path('check-guess/', CheckGuessView.as_view(), name='check_guess'),
 ]
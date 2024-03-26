from django.urls import path

from . import views
from .views import MapGameView, HomeView, CheckGuessView

urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),  # URL for the home page
    path('map-game/', MapGameView.as_view(), name='map_game'),  # URL for the map game page
    path('check-guess/', CheckGuessView.as_view(), name='check_guess'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
 ]
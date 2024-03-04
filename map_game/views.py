from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import TemplateView
from .models import CountryModels

def home(request):
    return render(request, 'home.html', context={})

class MapGameView(TemplateView):
    template_name = 'map_game.html'

class HomeView(TemplateView):
    template_name = 'home.html'
    model = CountryModels
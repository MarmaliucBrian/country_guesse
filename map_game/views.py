from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
import random

from map_game.models import CountryModels


class MapGameView(TemplateView):
    template_name = 'map_game.html'
    countries = [
        "Andorra", "Armenia", "Austria", "Belgium", "Bulgaria", "Bosnia and Herzegovina",
        "Belarus", "Switzerland", "Czech Republic", "Germany", "Denmark", "Estonia",
        "Finland", "United Kingdom", "Georgia", "Greece", "Croatia", "Hungary",
        "Ireland", "Iceland", "Italy", "Liechtenstein", "Lithuania", "Luxembourg",
        "Latvia", "Moldova", "Macedonia", "Montenegro", "Norway", "Poland",
        "Portugal", "Romania", "Serbia", "Slovakia", "Slovenia", "Sweden",
        "Turkey", "Ukraine", "Kosovo", "Netherlands", "Spain", "France", "Cyprus"
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        guessed_countries = self.request.session.get('guessed_countries', [])
        target_country_index = self.request.session.get('target_country_index', 0)

        if not guessed_countries:
            random.shuffle(self.countries)

        target_country = self.countries[target_country_index]
        context['target_country'] = target_country
        return context


class HomeView(TemplateView):
    template_name = 'home.html'
    model = CountryModels

class CheckGuessView(View):
    def post(self, request):
        # Get the clicked and target countries from the POST data
        clicked_country = request.POST.get('clicked_country')
        target_country = request.POST.get('target_country')

        # Retrieve guessed countries and target country index from session
        guessed_countries = request.session.get('guessed_countries', [])
        target_country_index = request.session.get('target_country_index', 0)

        # Compare the clicked and target countries (case-insensitive)
        if clicked_country.lower() == target_country.lower():
            # Append guessed country to the list and increment target country index
            guessed_countries.append(target_country)
            target_country_index += 1

            # Update session variables
            request.session['guessed_countries'] = guessed_countries
            request.session['target_country_index'] = target_country_index

            # Check if all countries have been guessed
            if target_country_index >= len(MapGameView.countries):
                # Game completed, send JSON response indicating completion
                return JsonResponse({'completed': True})
            else:
                # Game not completed, send JSON response indicating correct guess
                return JsonResponse({'correct_guess': True})
        else:
            # Send JSON response indicating incorrect guess
            return JsonResponse({'correct_guess': False})

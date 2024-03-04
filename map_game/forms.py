from django.forms import ModelForm

from map_game.models import CountryModels


class MapForm(ModelForm):
    class Meta:
        model = CountryModels
        fields = '__all__'
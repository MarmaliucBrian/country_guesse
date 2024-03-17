from django.db import models
from django.contrib.auth.models import User

class CountryModels(models.Model):
    name = models.CharField(max_length=100)
    position_x = models.IntegerField()
    position_y = models.IntegerField()

    def __str__(self):
        return self.name






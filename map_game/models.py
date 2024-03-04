from django.db import models

class CountryModels(models.Model):
    name = models.CharField(max_length=100)
    position_x = models.IntegerField()
    position_y = models.IntegerField()

    def __str__(self):
        return self.name
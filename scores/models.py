from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Scores(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"'{self.user.username}'s score: {self.score}"
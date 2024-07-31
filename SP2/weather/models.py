from django.db import models
from django.contrib.auth.models import User

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    date_searched = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    humidity = models.IntegerField()
    wind_speed = models.FloatField()

    def __str__(self):
        return f'{self.city} ({self.user.username})'

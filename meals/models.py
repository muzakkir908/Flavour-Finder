from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', null=True)
    meal_id = models.CharField(max_length=10)
    meal_name = models.CharField(max_length=100)
    meal_thumb = models.URLField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.meal_name
    
    class Meta:
        # Add this to ensure each user can only favorite a meal once
        unique_together = ['user', 'meal_id']
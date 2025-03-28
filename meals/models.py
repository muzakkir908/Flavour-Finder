from django.db import models

class Favorite(models.Model):
    meal_id = models.CharField(max_length=10)
    meal_name = models.CharField(max_length=100)
    meal_thumb = models.URLField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.meal_name
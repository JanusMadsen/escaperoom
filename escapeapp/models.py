from django.db import models

class Mushroom(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/mushrooms/')
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.name

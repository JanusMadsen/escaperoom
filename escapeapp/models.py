from django.db import models

class Mushroom(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/mushrooms/')
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class SourdoughStep(models.Model):
    name = models.CharField(max_length=100)
    correct_order = models.IntegerField()

    def __str__(self):
        return self.name
    
class BoardgameTrivia(models.Model):
    question = models.CharField(max_length=255)
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')])

    def __str__(self):
        return self.question
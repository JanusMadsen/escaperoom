from django.shortcuts import render, redirect
from .models import Mushroom
import random

def mushroom_puzzle(request):
    mushrooms = list(Mushroom.objects.all())
    options = random.sample(mushrooms, min(4, len(mushrooms)))  # Show 4 random mushrooms
    message = ''

    if request.method == 'POST':
        chosen_id = request.POST.get('mushroom')
        if Mushroom.objects.filter(id=chosen_id, is_correct=True).exists():
            message = 'Correct! You’ve found the right mushroom.'
            # Redirect or show next scene
        else:
            message = 'Not quite, try again!'

    return render(request, 'mushroom_puzzle.html', {
        'mushrooms': options,
        'message': message,
    })

from django.shortcuts import render, redirect
from .models import Mushroom, SourdoughStep, BoardgameTrivia
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

def sourdough_puzzle(request):
    steps = list(SourdoughStep.objects.all().order_by('?'))
    message = ''

    if request.method == 'POST':
        submitted_order = request.POST.getlist('step')
        correct_order = list(SourdoughStep.objects.all().order_by('correct_order').values_list('id', flat=True))

        if list(map(int, submitted_order)) == correct_order:
            message = 'Perfect! The sourdough is baked just right.'
            # Redirect or next scene logic here
        else:
            message = 'Hmm… the dough collapsed. Try again!'

    return render(request, 'sourdough_puzzle.html', {
        'steps': steps,
        'message': message,
    })

def boardgame_puzzle(request):
    questions = BoardgameTrivia.objects.all()
    message = ''
    correct = 0

    if request.method == 'POST':
        total = questions.count()
        for q in questions:
            answer = request.POST.get(f'question_{q.id}')
            if answer == q.correct_option:
                correct += 1
        if correct == total:
            message = 'You’re a true boardgame master!'
        else:
            message = f'You got {correct} out of {total} correct. Try again!'

    return render(request, 'boardgame_puzzle.html', {
        'questions': questions,
        'message': message,
    })

def berlin_half_puzzle(request):
    correct_time = "01:27:20"  # PB
    strava_time = "01:26:17" # Strava time
    message = ''
    success = False

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer.strip() == correct_time:
            message = "🏁 Perfect! You've just crossed the finish line!"
            success = True
        elif answer.strip() == strava_time:
            message = "⏱️ Close! That's your Strava time, but we need the official PB time."
            success = False
        else:
            message = "Hmm... that’s not quite the time we're looking for."

    return render(request, 'berlin_half_puzzle.html', {
        'message': message,
        'success': success,
    })

def summerhouse_final(request):
    return render(request, 'summerhouse_final.html')

def summerhouse_landing(request):
    success = False
    message = ''

    if request.method == 'POST':
        code = request.POST.get('code', '').strip().lower()
        if code == 'elgkig2023':  # Replace with your real unlock code
            return redirect('summerhouse_final')
        else:
            message = "That code doesn’t seem right."

    return render(request, 'summerhouse_landing.html', {
        'message': message
    })

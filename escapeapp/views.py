from django.shortcuts import render, redirect
from .models import Mushroom, SourdoughStep, BoardgameTrivia
import random
import time
from datetime import datetime, timedelta

def mushroom_puzzle(request):
    # Define mushrooms with file, position, and optional number
    mushrooms = [
    {"file": "mushroom1.png", "x": 100, "y": 150, "number": "1"},
    {"file": "mushroom2.png", "x": 250, "y": 400, "number": "2"},
    {"file": "mushroom3.png", "x": 380, "y": 220, "number": "3"},
    {"file": "mushroom4.png", "x": 600, "y": 180, "number": "4"},
    {"file": "mushroom5.png", "x": 150, "y": 550, "number": "5"},
    {"file": "mushroom6.png", "x": 480, "y": 510, "number": "6"},
    {"file": "mushroom7.png", "x": 750, "y": 300, "number": "7"},
    {"file": "mushroom8.png", "x": 620, "y": 600, "number": "8"},
    {"file": "mushroom9.png", "x": 300, "y": 650, "number": "9"},
    {"file": "mushroom10.png", "x": 850, "y": 420,"number": "10"},
    ]
    correct_code = "5832"
    message = ""
    code_input = ""

    if request.method == "POST":
        code_input = request.POST.get("code", "")
        if code_input == correct_code:
            message = "✅ Correct! The mushroom code is accepted."
        else:
            message = "❌ That code is not right yet. Keep looking!"

    return render(request, "mushroom_puzzle.html", {
        "mushrooms": mushrooms,
        "message": message,
        "code_input": code_input,
    })

# Fake wait times in seconds
WAIT_TIMES = {
    "feed": 30,
    "mix": 10,
    "folds": 5,
    "shape": 10,
    "cold_proof": 60,
}

def sourdough_puzzle(request):
# Define correct sourdough step sequence
    steps = [
        {"name": "Feed Starter", "wait": None},
        {"name": "Mix Dough", "wait": 240},  # 4 hours
        {"name": "Fold Dough", "wait": 30},  # needs 6–8 repetitions
        {"name": "Preshape", "wait": 30},
        {"name": "Shape + Cold Proof", "wait": 30}, 
        {"name": "Bake", "wait": 720}] # 12 hours
    

    if "sourdough_state" not in request.session:
        request.session["sourdough_state"] = {
            "current_step": 0,
            "fold_count": 0,
            "message": "",
            "image": "sourdough_starter.png",
            "failed": False,
            "completed": False
        }

    state = request.session["sourdough_state"]

    if request.method == "POST":
        if "reset" in request.POST:
            del request.session["sourdough_state"]
            return redirect("sourdough_puzzle")

        if state.get("completed"):
            state["message"] = "🎉 You already completed the puzzle!"
        else:
            entered_minutes = request.POST.get("minutes")
            selected_step = request.POST.get("step")

            try:
                entered_minutes = int(entered_minutes)
            except (ValueError, TypeError):
                state["message"] = "⚠️ Enter a valid number of minutes."
                request.session.modified = True
                return render(request, "sourdough_puzzle.html", {"state": state, "steps": steps})

            current = state["current_step"]

            # ✅ prevent out of range access
            if current >= len(steps):
                state["message"] = "🎉 Puzzle already finished!"
                state["completed"] = True
            else:
                expected_step = steps[current]["name"]
                expected_wait = steps[current]["wait"]

                if selected_step != expected_step:
                    state["message"] = f"❌ Not the correct step right now."
                    state["failed"] = True
                else:
                    # Special folding logic
                    if selected_step == "Fold Dough":
                        if abs(entered_minutes - 30) > 10:
                            state["message"] = "❌ Wrong folding time. Dough collapsed!"
                            state["failed"] = True
                        else:
                            state["fold_count"] += 1
                            state["message"] = f"✅ Fold {state['fold_count']} done."
                            state["image"] = "sourdough_fold.png"
                            if state["fold_count"] >= 6:
                                state["current_step"] += 1
                                state["message"] = f"✅ Fold {state['fold_count']} done."
                                
                    else:
                        if expected_wait is None or abs(entered_minutes - expected_wait) <= 10:
                            state["current_step"] += 1
                            state["message"] = f"✅ {selected_step} successful!"

                            # ✅ Show rise image right after feeding starter
                            if selected_step == "Feed Starter":
                                state["image"] = "sourdough_rise.png"
                            
                            elif selected_step == "Shape + Cold Proof":
                                state["image"] = "coldproofing.png"

                            elif selected_step == "Bake":
                                state["completed"] = True
                                if state["failed"]:
                                    state["image"] = "bread_failed.png"  # flat sourdough if earlier mistake
                                    state["message"] = "❌ The bread collapsed due to earlier mistakes!"
                                else:
                                    state["image"] = "bread_baked.png"   # success
                                    state["message"] = "🎉 Perfect sourdough bread baked!"
                        else:
                            state["message"] = f"❌ Wrong timing for {selected_step}."
                            state["failed"] = True

    request.session.modified = True
    return render(request, "sourdough_puzzle.html", {
        "state": state,
        "steps": steps
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

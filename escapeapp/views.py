from django.shortcuts import render, redirect
from .models import Mushroom, SourdoughStep, BoardgameTrivia
import random
import time
from datetime import datetime, timedelta

def home(request):
    message = ""
    if request.method == "POST":
        answer = request.POST.get("answer", "").strip().lower()
        if answer == "perikumvej":
            return redirect("summerhouse_landing")
        else:
            message = "❌ Det er ikke den rigtige vej i Nordjylland."
    
    return render(request, "home.html", {"message": message})

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
    {"file": "mushroom9.png", "x": 300, "y": 650, "number": "10"},
    {"file": "mushroom10.png", "x": 850, "y": 420,"number": "9"},
    ]
    correct_code = "7593"
    message = ""
    code_input = ""

    if request.method == "POST":
        code_input = request.POST.get("code", "")
        if code_input == correct_code:
            message = "✅ Det er korrekt! Du har fundet det rigtige kodeord. hintet er 'M'"
        else:
            message = "❌ Den kode er ikke korrekt. Mon du har en bog med svampe?"

    return render(request, "mushroom_puzzle.html", {
        "mushrooms": mushrooms,
        "message": message,
        "code_input": code_input,
    })


def sourdough_puzzle(request):
    # Definer korrekt surdejssekvens
    steps = [
        {"name": "Fodr Surdej", "wait": None},
        {"name": "Mix Dej", "wait": 240},  # 4 timer
        {"name": "Fold Dej", "wait": 30},  # 4–7 gentagelser
        {"name": "Preshape", "wait": 30},
        {"name": "Shape og koldhæv", "wait": 20},
        {"name": "Bag", "wait": 720}       # 12 timer
    ]

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
            state["message"] = "🎉 Du har allerede gennemført surdejspuslespillet!"
        else:
            entered_minutes = request.POST.get("minutes")
            selected_step = request.POST.get("step")

            try:
                entered_minutes = int(entered_minutes)
            except (ValueError, TypeError):
                state["message"] = "⚠️ Indtast et gyldigt antal minutter."
                request.session.modified = True
                return render(request, "sourdough_puzzle.html", {"state": state, "steps": steps})

            current = state["current_step"]

            # ✅ undgå out of range fejl
            if current >= len(steps):
                state["message"] = "🎉 Puslespillet er allerede færdigt!"
                state["completed"] = True
            else:
                expected_step = steps[current]["name"]
                expected_wait = steps[current]["wait"]

                if selected_step != expected_step and selected_step != "Fold Dej":
                    state["message"] = f"❌ Det er ikke det rigtige trin lige nu."
                    state["failed"] = True
                else:
                    # 👉 Foldelogik
                    if selected_step == "Fold Dej":
                        if abs(entered_minutes - 30) > 10:
                            state["message"] = "❌ Forkert foldetid. Dejen faldt sammen!"
                            state["failed"] = True
                        else:
                            state["fold_count"] += 1
                            state["message"] = f"✅ Fold {state['fold_count']} udført."
                            state["image"] = "sourdough_fold.png"

                            # Når man har foldet mellem 4 og 7 gange → gå videre
                            if 4 == state["fold_count"]:
                                state["current_step"] += 1
                                state["message"] = f"✅ {state['fold_count']} fold udført."
                            elif 7 >= state["fold_count"] > 4:
                                state["message"] = f"✅ {state['fold_count']} fold udført."
                            elif state["fold_count"] > 7:
                                state["message"] = "❌ Du har foldet for mange gange, dejen blev overarbejdet!"
                                state["failed"] = True

                    else:
                        if expected_wait is None or abs(entered_minutes - expected_wait) <= 10:
                            state["current_step"] += 1
                            state["message"] = f"✅ {selected_step} lykkedes!"

                            # ✅ Vis billeder for de enkelte trin
                            if selected_step == "Fodr Surdej":
                                state["image"] = "sourdough_rise.png"

                            elif selected_step == "Mix Dej":
                                state["image"] = "mix.png"

                            elif selected_step == "Preshape":
                                state["image"] = "preshape.png"

                            elif selected_step == "Shape og koldhæv":
                                state["image"] = "coldproofing.png"

                            elif selected_step == "Bag":
                                state["completed"] = True
                                if state["failed"]:
                                    state["image"] = "bread_failed.png"
                                    state["message"] = "❌ Brødet faldt sammen pga. tidligere fejl!"
                                else:
                                    state["image"] = "bread_baked.png"
                                    state["message"] = "🎉 Perfekt surdejsbrød bagt! hint er 'e'"
                        else:
                            state["message"] = f"❌ Forkert tid for {selected_step}."
                            state["failed"] = True

    request.session.modified = True
    return render(request, "sourdough_puzzle.html", {
        "state": state,
        "steps": steps
    })



def boardgame_puzzle(request):
    games = [
        {
            "name": "Carcassonne",
            "image": "carcassonne.jpg",
            "clues": ["Riddere og landevejsrøvere", "floden", "Meeples"]
        },
        {
            "name": "7 Wonders Duel",
            "image": "7wondersduel.jpg",
            "clues": ["To spillere", "3 tidsaldrer", "altan i regnvejr"]
        },
        {
            "name": "Splendor Duel",
            "image": "splendorduel.jpg",
            "clues": ["3 måder at vinde på", "ædelstene", "kortkøb"]
        },
        {
            "name": "Kvaksalver",
            "image": "kvaksalver.jpg",
            "clues": ["gurkemejemand", "natsværmer", "hyldeblomst"]
        },
        {
            "name": "Hitster",
            "image": "hitster.jpg",
            "clues": ["Årstal", "ørelyt", "ubegrænsede spillere"]
        },
        {
            "name": "Ticket to Ride",
            "image": "ticket_to_ride.jpg",
            "clues": ["hemmelige kort", "mange farver", "togrejser"]
        },
    ]

    # Init progress, hvis den ikke findes
    if "boardgame_progress" not in request.session:
        request.session["boardgame_progress"] = 0

    progress = request.session.get("boardgame_progress", 0)
    finished = progress >= len(games)
    current_game = games[progress] if not finished else None

    message = ""

    if request.method == "POST":
        if "reset" in request.POST:
            request.session["boardgame_progress"] = 0   # ✅ rettet
            message = "🔄 Spillet er nulstillet. Start forfra!"
            finished = False
            current_game = games[0]
        elif finished:
            return render(request, "boardgame_puzzle.html", {
                "game": None,
                "message": "🎉 Tillykke, du klarede alle spil!",
                "progress": progress,
                "total_games": len(games),
                "finished": True,
                "final_clue": "🔑 Dit clue: 'i' bogstavet i koden",
            })
        else:
            answer = request.POST.get("answer", "").strip().lower()
            correct = current_game["name"].lower()

            if answer == correct:
                progress += 1
                request.session["boardgame_progress"] = progress
                return redirect("boardgame_puzzle")
            else:
                message = "❌ Ikke helt rigtigt. Prøv igen!"

    return render(request, "boardgame_puzzle.html", {
        "game": current_game,
        "message": message,
        "progress": progress,
        "total_games": len(games),
        "finished": finished,
        "final_clue": "🔑 Dit clue: B bogstavet i koden"
    })



def berlin_half_puzzle(request):
    correct_time = "01:27:20"  # PB
    strava_time = "01:26:17" # Strava time
    message = ''
    success = False

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer.strip() == correct_time:
            message = "🏁 Perfekt du har fundet den rigtige tid. hintet er 'n'"
            success = True
        elif answer.strip() == strava_time:
            message = "⏱️ Tæt på! Det er din Strava tid. Vi skal have din officielle tid fra løbet."
            success = False
        else:
            message = "Hmm... det er ikke helt rigtigt. Prøv igen."

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
        if code == 'mien':  # Replace with your real unlock code
            return redirect('summerhouse_final')
        else:
            message = "That code doesn’t seem right."

    return render(request, 'summerhouse_landing.html', {
        'message': message
    })

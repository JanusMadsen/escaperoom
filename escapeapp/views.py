from django.shortcuts import render, redirect
from .models import RoomState

# Reset the level (door closed) at server startup
def reset_room_state():
    state, _ = RoomState.objects.get_or_create(pk=1)
    state.door_open = False
    state.save()

try:
    reset_room_state()
except Exception:
    # Database might not be ready during migrations, ignore errors at import time
    pass

def home(request):
    # Get or create the room state (single room for simplicity)
    state, _ = RoomState.objects.get_or_create(pk=1)
    message = ""
    if request.method == "POST":
        code = request.POST.get("code", "")
        state.user_input = code
        if code == state.lock_code:
            state.door_open = True
            message = "Correct code! The door is open."
        else:
            state.door_open = False
            message = "Incorrect code. Try again."
        state.save()
        return render(request, 'home.html', {'door_open': state.door_open, 'message': message, 'user_input': state.user_input})
    return render(request, 'home.html', {'door_open': state.door_open, 'message': message, 'user_input': state.user_input})

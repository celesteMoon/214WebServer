from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def game_view(request, game_id):
    return render(request, 'rps/game.html', {'game_id': game_id})

@login_required
def lobby_view(request):
    return render(request, 'rps/lobby.html')
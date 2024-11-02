from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def profile_view(request, username):
    return render(request, 'user_profile/profile.html', {'username': username})
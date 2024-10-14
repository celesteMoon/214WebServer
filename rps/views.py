from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def rps_view(request):
    if request.method == 'POST':
        pass
    return render(request, 'rps/rps.html')
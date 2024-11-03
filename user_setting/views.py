from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def setting_view(request):
    return render(request, 'user_setting/setting.html')
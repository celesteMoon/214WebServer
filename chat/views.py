from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Message

@login_required
def chat_view(request):
    if request.method == 'POST':
        username = request.user.username
        content = request.POST.get('content')
        timestamp = request.POST.get('timestamp')
        Message.objects.create(username=username, content=content, timestamp=timestamp)
        return redirect('chat')

    messages = Message.objects.all().order_by('-timestamp')
    return render(request, 'chat/chat.html', {'messages': messages})
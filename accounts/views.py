from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
from .forms import LoginForm, UserRegistrationForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat')  # 登录后跳转到聊天室
            else:
                messages.error(request, "无效的用户名或密码")
        else:
            messages.error(request, "无效的表单输入")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # 注销后跳转到登录页面

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # 使用哈希密码
            user.save()
            return redirect('login')  # 重定向到登录页面
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request, username):
    return render(request, 'accounts/profile.html', {'username': username})
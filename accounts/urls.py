from django.urls import path
from .views import login_view, logout_view, register, profile_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('profile/<str:username>/', profile_view, name='profile')
]

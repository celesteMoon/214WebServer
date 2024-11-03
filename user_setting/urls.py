from django.urls import path
from .views import setting_view

urlpatterns = [
    path('', setting_view, name='setting')
]

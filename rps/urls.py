from django.urls import path
from .views import rps_view

urlpatterns = [
    path('', rps_view, name='rps'),
]
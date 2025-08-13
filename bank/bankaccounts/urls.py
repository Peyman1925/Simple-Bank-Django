from django.urls import path
from .views import *

urlpatterns = [
    path('transfer/', transfer_money, name='transfer'),
]
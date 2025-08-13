from django.urls import path
from .views import *

app_name = 'webaccounts'

urlpatterns = [
    path('register/', signup, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
]
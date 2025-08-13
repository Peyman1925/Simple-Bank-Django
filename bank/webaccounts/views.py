from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
from bankaccounts.models import *
from django.core.mail import send_mail
from django.conf import settings

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            try:
                subject = 'Welcome to Our Bank'
                message = f'Hello {user.username},\n\nWelcome to Our Bank!\n\nYour account has been successfully created.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                
                send_mail(
                    subject,
                    message,
                    email_from,
                    recipient_list,
                    fail_silently=False
                )
                messages.success(request, 'Registration successful! Welcome email sent.')
            except Exception as e:
                messages.warning(request, f'Account created but email not sent: {str(e)}')
            
            auth.login(request, user)
            return redirect('webaccounts:profile')
    else:
        form = SignUpForm()
    return render(request, 'webaccounts/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.login(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Password or username is incorrect')
    else:
        form = LoginForm()
    return render(request, 'webaccounts/login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('webaccounts:login')

@login_required
def profile(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-created_at')[:10]
    return render(request, 'webaccounts/profile.html', {
        'user': user,
        'transactions': transactions
    })
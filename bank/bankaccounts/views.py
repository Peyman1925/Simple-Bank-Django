from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import *
from webaccounts.models import *
from .models import *

@login_required
def transfer_money(request):
    if request.method == 'POST':
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            amount = form.cleaned_data['amount']
            
            with transaction.atomic():

                request.user.wallet -= amount
                request.user.save()
                
                recipient.wallet += amount
                recipient.save()
                
                Transaction.objects.create(
                    user=request.user,
                    money=-amount,
                )
                Transaction.objects.create(
                    user=recipient,
                    money=amount,
                )
            
            messages.success(request, 'The transfer was successful.')
            return redirect('webaccounts:profile')
    else:
        form = TransferForm(user=request.user)
    
    return render(request, 'bankaccounts/transfer.html', {'form': form})
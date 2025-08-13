from django import forms
from django.core.exceptions import ValidationError
from webaccounts.models import CustomUser
from django.db import models

class TransferForm(forms.Form):
    recipient = forms.CharField(
        label='Recipient username or mobile number',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    amount = forms.DecimalField(
        label='Amount',
        min_value=1,
        max_digits=15,
        decimal_places=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TransferForm, self).__init__(*args, **kwargs)

    def clean_recipient(self):
        recipient = self.cleaned_data['recipient']
        try:
            return CustomUser.objects.get(
                models.Q(username=recipient) | 
                models.Q(phone_number=recipient)
            )
        except CustomUser.DoesNotExist:
            raise ValidationError('user is not found')

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if self.user.wallet < amount:
            raise ValidationError('Not enough inventory.')
        return amount
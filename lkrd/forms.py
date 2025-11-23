from django import forms
from users.models import User
from .models import Transaction

class TransactionForm(forms.Form):
    sender_card = forms.CharField()
    receiver_card = forms.CharField()
    amount = forms.DecimalField()
    comment = forms.CharField(required=False)
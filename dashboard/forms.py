from django import forms  
from .models import Loan, Ticket, FixedDeposit, Contact, Wallet, CryptoWithdrawal

class ExchangeForm(forms.Form):
    exchange_from = forms.CharField(
        widget=forms.Select(
            attrs={'class': 'form-control auto-select select2'},
            choices=[
                ('USD', 'USD'),
                ('EUR', 'EUR'),
                ('INR','INR')
            ],
        ),
        label='Exchange From',
    )
    exchange_to = forms.CharField(
        widget=forms.Select(
            attrs={'class': 'form-control auto-select select2',},
            choices=[
                ('USD', 'USD'),
                ('EUR', 'EUR'),
                ('INR','INR')
            ]
        ),
        label='Exchange To'
    )
    amount = forms.CharField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    ) 
    exchanged_amount = forms.CharField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    
    
class LoanForm(forms.ModelForm):
    
    class Meta:
        model = Loan
        exclude = ('collector', 'status', 'created_at', 'last_updated', 'amount_paid')
    
class TicketForm(forms.ModelForm):
    
    class Meta:
        model = Ticket 
        exclude = ('creator', 'created_at', 'last_updated', 'status')
        
        
class FixedDepositForm(forms.ModelForm):
    
    class Meta:
        model = FixedDeposit 
        exclude = ('depositor', 'created_at', 'last_updated')
        
class ContactForm(forms.ModelForm):
    
    class Meta:
        model = Contact 
        exclude = ('id',)
        

class WalletForm(forms.ModelForm):
    
    class Meta:
        model = Wallet 
        exclude = ('id', 'holder', 'created_at', 'last_updated')
        
        
class WithdrawalForm(forms.ModelForm):
    
    class Meta:
        model = CryptoWithdrawal 
        exclude = ('id', 'user', 'withdrawal_date', 'transaction_hash', 'status')
        
        
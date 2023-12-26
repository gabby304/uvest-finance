from django.contrib import admin
from .models import Account, Loan, Ticket, Contact, ActivationCard, Wallet, CryptoWithdrawal
# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_number', 'account_holder', 'usd_account', 'euro_account', 'inr_account', 'is_active')
    
    
@admin.register(Loan) 
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan_product', 'amount', 'collector', 'status')
    
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'creator', 'created_at')
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'subject')
    
    
@admin.register(ActivationCard)
class ActivationCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'card_type', 'card_holder', 'card_number', 'valid_thru')

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'holder', 'wallet_name', 'crypto', 'address')
    
@admin.register(CryptoWithdrawal)
class CryptoWithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'wallet', 'withdrawal_date', 'status')
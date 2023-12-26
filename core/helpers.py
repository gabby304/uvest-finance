import random
from dashboard.models import Account
from django.shortcuts import get_object_or_404
from django.core import exceptions



class AccountNumber:
    
    def __init__(self, instance):
        self.accounts = instance.objects.filter()
    
    @staticmethod
    def get_random_account():
        prefix = random.randint(10, 99)
        number = random.randint(1e9, 1e10 - 1)
        check = int((prefix * 1e10) + number) % 97
        return f"{prefix:0>2d}{number:0>6d}{check:0>2d}"
    
    def create_account(self):
        while True:
            account = self.get_random_account()
            if not self.accounts.filter(account_number=account).exists():
                return account
    
    
class Exchange: 
    
    def __init__(self, exchange_from, exchange_to, amount, exchanged_amount) -> None:
        self.exchange_from = exchange_from
        self.exchange_to = exchange_to 
        self.amount = amount 
        self.exchanged_amount = exchanged_amount
        
    def resolve(self):
        currency_list = ['USD', 'EUR', 'INR']
        resolve_from = any(ele == self.exchange_from for ele in currency_list)
        resolve_to = any(ele == self.exchange_to for ele in currency_list)
        exception_reason = ''
        
        if not (resolve_from and resolve_to):
            exception_reason = "Allowed currencies are 'USD', 'EUR' and 'INR' only !"
            return (False, exception_reason)
        if self.exchange_from == self.exchange_to:
            exception_reason = "Cannot exchange to the same currency !"
            return (False, exception_reason)
        return (True, 'passed for exchange')
    
    
    def perform_exchange(self, account_holder) -> None:
        check_resolve = self.resolve()
        reason = check_resolve[1]
        if not check_resolve[0]:
            raise exceptions.ValidationError(f"{reason}")
        
        account = get_object_or_404(Account, account_holder=account_holder) 
        account_dict = {
            'USD': 'usd_account',
            'EUR': 'euro_account',
            'INR': 'inr_account'
        }
        # value for exchange-from
        value_from = getattr(account, account_dict[self.exchange_from]) 
        # value for exchange-to
        value_to = getattr(account, account_dict[self.exchange_to]) 
        
        if float(value_from) < float(self.amount):
            raise exceptions.ValidationError(f"Insufficient balance in {self.exchange_from} account")
        
        # withdraw from the exchange-from account and Set the attribute to 
        # the account-type 
        value_from -= float(self.amount) 
        setattr(account, account_dict[self.exchange_from], value_from)
        
        # Add to the exchange-to account and set the attribute 
        # to the account-type 
        value_to += float(self.exchanged_amount)
        setattr(account, account_dict[self.exchange_to], value_to)
        # Save the values to the database 
        account.save()
        
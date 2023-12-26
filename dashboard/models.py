from django.db import models
from django.conf import settings
from shortuuidfield import ShortUUIDField
import contextlib 
from .validators import validate_proposed_payment_date
import uuid 
from datetime import date 
from calendar import isleap 
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


def add_years(d: date, years: int) -> date:
    """Add years to a date."""
    year = d.year + years
    # if leap day and the new year is not leap, replace year and day
    # otherwise, only replace year
    if d.month == 2 and d.day == 29 and not isleap(year):
        return d.replace(year=year, day=28)
    return d.replace(year=year)


class Account(models.Model): 
        
    id = ShortUUIDField(primary_key=True, max_length=6, editable=False)
    account_number = models.CharField(max_length=20, unique=True) 
    account_holder = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    usd_account = models.FloatField(default=0, verbose_name='Dollar Account')
    euro_account = models.FloatField(default=0, verbose_name='Euro Account')
    inr_account = models.FloatField(default=0, verbose_name='Rupee Account')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    card_activated = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        from core.helpers import AccountNumber
        # create an account number for the user
        if not Account.objects.filter(id=self.id).exists():
            account = AccountNumber(Account)
            self.account_number = account.create_account()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.account_holder}'s Account ({self.account_number})"
    

class ActivationCard(models.Model):
    
    class CardType(models.TextChoices):
        BASIC_CARD = "Basic Card", "Basic Card"
        STANDARD_CARD = "Standard Card", "Standard Card"
    
    id = ShortUUIDField(primary_key=True, max_length=6, editable=False)
    card_type  = models.CharField(max_length=20, choices=CardType.choices)
    card_holder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    valid_thru = models.DateField(null=True, blank=True)    
    
    def save(self, *args, **kwargs):
        # create default random 16 digit string for card number
        
        random_str = str(
                        uuid.uuid4().int
                        )[:self._meta.get_field('card_number').max_length]
        self.card_number = random_str
        
        # create valid_thru date for card
        if self.valid_thru is not None:
            self.valid_thru = add_years(date.today(), 1)
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f'{self.card_holder} ({self.card_type})'

    
    
class Loan(models.Model):
    
    class LoanProduct(models.TextChoices):
        STUDENT_LOAN = 'Student Loan', 'Student Loan',
        BUSINESS_LOAN = 'Business Loan', 'Business Loan'
        ENTERPRISE_LOAN = 'Enterprise Loan', 'Enterprise Loan'
        
    class Currency(models.TextChoices):
        USD = 'USD', 'USD'
        EUR = 'EUR', 'EUR'
        INR = 'INR', 'INR'
        
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        COMPLETED = "Completed", "Completed"
    
    id = ShortUUIDField(primary_key=True, max_length=6, editable=False)
    loan_product = models.CharField(max_length=20)
    identity = models.FileField(upload_to='files/identity')
    currency = models.CharField(max_length=15, choices=Currency.choices, default=Currency.USD)
    amount = models.FloatField()
    amount_paid = models.FloatField(default=0)
    proposed_payment_date = models.DateField(validators=[validate_proposed_payment_date])
    description = models.TextField()
    collector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    @property
    def balance(self):
        return self.amount - self.amount_paid
    
    def save(self, *args, **kwargs):
        """Deletes old identity file when making an update to identity"""
        with contextlib.suppress(Exception):
            old_file = Loan.objects.get(id=self.id)
            if old_file.identity != self.identity:
                old_file.identity.delete(save=False)
                
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self.loan_product} for {self.collector}'     
    

class Ticket(models.Model):
    
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        COMPLETED = "Completed", "Completed"
        
    id = ShortUUIDField(primary_key=True, max_length=6, editable=False) 
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=200)
    attachment = models.FileField(upload_to='files/tickets')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """Deletes old attachment file when making an update to attachment"""
        with contextlib.suppress(Exception):
            old_file = Ticket.objects.get(id=self.id)
            if old_file.attachment != self.attachment:
                old_file.attachment.delete(save=False)
        super().save(*args, **kwargs)

    
    def __str__(self) -> str:
        return f'TIcket no. {self.id} by {self.creator}'
    
    

class FixedDeposit(models.Model):
    
    class DepositPlan(models.TextChoices):
        BASIC = 'Basic', 'Basic'
        STANDARD = 'Standard', 'Standard'
        PROFESSIONAL = 'Professional', 'Professional'
        
    class Currency(models.TextChoices):
        USD = 'USD', 'USD'
        EUR = 'EUR', 'EUR'
        INR = 'INR', 'INR'
    
    id = ShortUUIDField(primary_key=True, max_length=6, editable=False) 
    deposit_plan = models.CharField(max_length=20, choices=DepositPlan.choices)
    currency = models.CharField(max_length=10, choices=Currency.choices)
    deposit_amount = models.FloatField()
    remarks = models.CharField(max_length=200)
    attachment = models.FileField(upload_to='files/deposits')
    depositor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.deposit_plan} for {self.depositor}'
    

class Contact(models.Model):
    id = ShortUUIDField(primary_key=True, max_length=6, editable=False) 
    fullname = models.CharField(max_length=30)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) -> str:
        return self.fullname
    

class Wallet(models.Model):
    
    class Crypto(models.TextChoices):
        BITCOIN = 'BTC', 'BTC'
        TETHER = 'USDT (TRC20)', 'USDT (TRC20)'
    
    wallet_name = models.CharField(max_length=20, null=True, blank=True, unique=True)
    crypto = models.CharField(max_length=20, choices=Crypto.choices)
    address = models.CharField(max_length=100)
    holder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        unique_together = ('crypto', 'address')
        
    def save(self, *args, **kwargs):
        if self.wallet_name is None:
            suffix = self.address[:4]
            self.wallet_name = f'Wallet-{suffix}'
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self.wallet_name} - {self.holder}'
    

class CryptoWithdrawal(models.Model):
    id = ShortUUIDField(primary_key=True, max_length=6, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    withdrawal_date = models.DateTimeField(auto_now_add=True)
    transaction_hash = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ])
    
    def save(self, *args, **kwargs):
        self.transaction_hash = self.id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount} {self.wallet} - {self.status}"
    

    
    
    

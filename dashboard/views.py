from typing import Any, Dict
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, FormView, CreateView, ListView, View
from .models import Account, Loan, Ticket, Contact, ActivationCard, Wallet, CryptoWithdrawal
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ExchangeForm, LoanForm, TicketForm, ContactForm, WalletForm, WithdrawalForm
from django.contrib import messages
from core.helpers import Exchange
from django.urls import reverse_lazy
from django.conf import settings
from django.urls import reverse
import requests 
import json
from coinbase_commerce.client import Client
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.


class HomeView(TemplateView):
    template_name = 'dashboard/home.html'
    
class ServiceView(TemplateView):
    template_name = 'dashboard/service.html'
    
class AboutView(TemplateView):
    template_name = 'dashboard/about.html'
    
class FAQView(TemplateView):
    template_name = 'dashboard/faq.html'
    
class TermsView(TemplateView):
    template_name = 'dashboard/terms.html'
    
class PrivacyPolicyView(TemplateView):
    template_name = 'dashboard/privacy-policy.html'
    
class WithdrawalPolicyView(TemplateView):
    template_name = 'dashboard/withdrawal-policy.html'
    
class FundingPolicyView(TemplateView):
    template_name = 'dashboard/funding-policy.html'
    
class TransactionReportView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/transactions-report.html'
    
class UserVerifiedMixin(UserPassesTestMixin, LoginRequiredMixin):
    
    def test_func(self) -> bool:
        return self.request.user.is_verified 
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, 'Please verify your email address!')
        return redirect('dashboard')
     

class DPSSchemePlanView(UserVerifiedMixin, View):
    
    def get(self, request):
        try:
            client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
            starter_checkout = client.checkout.retrieve(settings.COINBASE_CHECKOUT_ID_STARTER)
            basic_checkout = client.checkout.retrieve(settings.COINBASE_CHECKOUT_ID_BASIC)
            enterprise_checkout = client.checkout.retrieve(settings.COINBASE_CHECKOUT_ID_ENTERPRISE)
            starter_checkout_link = f'https://commerce.coinbase.com/checkout/{starter_checkout.id}'
            basic_checkout_link = f'https://commerce.coinbase.com/checkout/{basic_checkout.id}'
            enterprise_checkout_link = f'https://commerce.coinbase.com/checkout/{enterprise_checkout.id}'
            
            return render(request, 'dashboard/plans.html', {
                'starter_checkout_link': starter_checkout_link,
                'basic_checkout_link': basic_checkout_link,
                'enterprise_checkout_link': enterprise_checkout_link
            })
        except Exception:
            messages.error(request, 'Connectivity while Error loading DPS plans')
            return redirect('dashboard')
        
    
class DPSSchemesView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dps-schemes.html'


class ApplyFixedDepositView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/apply-fixed-deposit.html'
    
class FixedDepositsHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/history.html'
    
class AutomaticDepositView(LoginRequiredMixin, View):
    
    def get(self, request):
        try:
            client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
            deposit_checkout = client.checkout.retrieve(settings.COINBASE_CHECKOUT_ID_DEPOSIT)
            deposit_checkout_link = f'https://commerce.coinbase.com/checkout/{deposit_checkout.id}'
            
            return render(request, 'dashboard/automatic-deposit.html', {
                'deposit_checkout_link': deposit_checkout_link,
            })
        except Exception:
            messages.error(request, 'Connectivity while Error loading DPS plans')
            return redirect('dashboard')
      
    
class WithdrawalFormView(UserVerifiedMixin, CreateView):
    template_name = 'dashboard/withdraw-money.html'
    form_class = WithdrawalForm
    success_url = reverse_lazy('dashboard')
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data = super(WithdrawalFormView, self).get_context_data(**kwargs)
        data['withdrawal_form'] = data.get('form')
        
        wallets = Wallet.objects.filter(holder=self.request.user)
        data['wallets'] = wallets
        return data 
    
    def form_invalid(self, form: WithdrawalForm) -> HttpResponse:
        messages.error(self.request, form.errors)
        return redirect('withdrawal')
    
    def form_valid(self, form: WithdrawalForm) -> HttpResponse:
        self.object = form.save(commit=False) 
        self.object.user = self.request.user 
        self.object.save()
        messages.success(self.request, 'Your Withdrawal is being processed, you will receive an email shortly.')
        return redirect(self.get_success_url())   
    
    
    
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data['loans'] = Loan.objects.filter(collector=self.request.user) 
        data['account'] = get_object_or_404(Account, account_holder=self.request.user)
        return data 
    
    

class ExchangeView(UserVerifiedMixin, FormView):
    template_name = 'dashboard/exchange-money.html'
    form_class = ExchangeForm  
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data = super(ExchangeView, self).get_context_data(**kwargs)
        data['exchange_form'] = data.get('form')
        return data 
    
    def form_invalid(self, form: ExchangeForm) -> HttpResponse:
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def form_valid(self, form: ExchangeForm) -> HttpResponse:
        exchange_from, exchange_to = form.cleaned_data["exchange_from"], form.cleaned_data['exchange_to']
        amount, exchanged_amount = form.cleaned_data['amount'], form.cleaned_data['exchanged_amount']
        exchange = Exchange(
                            exchange_from=exchange_from, 
                            exchange_to=exchange_to, 
                            amount=amount,
                            exchanged_amount=exchanged_amount
                            )
        exchange.perform_exchange(self.request.user)
        messages.success(self.request, f'You have successfully converted {amount} {exchange_from} to {exchange_to}')
        return redirect('dashboard')
        
           
class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'dashboard/contact.html'
    success_url = reverse_lazy('contact')
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data = super(ContactView, self).get_context_data(**kwargs)
        data['contact_form'] = data.get('form')
        return data 
    
    def form_invalid(self, form: ContactForm) -> HttpResponse:
        messages.error(self.request, form.errors)
        return redirect('contact')
    
    def form_valid(self, form: ContactForm) -> HttpResponse:
        messages.success(self.request, 'Message successfully sent, you will receive a response shortly')
        return super().form_valid(form)
    
    
    
class ActivateCardView(UserVerifiedMixin, View):
    
    def get(self, request: HttpRequest) -> HttpResponse:
        domain_url = request.build_absolute_uri(reverse('homepage'))
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CC-Api-Key': settings.COINBASE_COMMERCE_API_KEY
        }
        data_list = [
            {
            'name': 'Basic Card Activation',
            'metadata': {
                'customer_id': str(request.user.pk),
                'customer_username': request.user.email,
            },
            'description': 'You need to make a deposit of $1050.00 in order to activate your Basic account',
            'local_price': {
                'amount': '1050.00',
                'currency': 'USD'
            },
            'pricing_type': 'fixed_price',
            'redirect_url': f'{domain_url}customer/account-activation/success/',
            'cancel_url': f'{domain_url}customer/account-activation/cancel/'
            },
            {
            'name': 'Standard Card Activation',
            'metadata': {
                'customer_id': str(request.user.pk),
                'customer_username': request.user.email,
            },
            'description': 'You need to make a minimum deposit of $2550.00 in order to activate your Standard account',
            'local_price': {
                'amount': '2550.00',
                'currency': 'USD'
            },
            'pricing_type': 'fixed_price',
            'redirect_url': f'{domain_url}customer/account-activation/success/',
            'cancel_url': f'{domain_url}customer/account-activation/cancel/'
            }
        
        ]
        
        try:
            responses = []
            for data_dict in data_list:
                payload = json.dumps(data_dict)
                res = requests.post(url='https://api.commerce.coinbase.com/charges', data=payload, headers=headers)
                data = res.json()['data']
                responses.append(data)
            return render(request, 'dashboard/activate-card.html', {
                'charges': responses
            })
        except Exception:
            messages.error(request, "Error connecting to coinbase")
            return render(request, 'dashboard/activate-card.html', {
                'error': "Error connecting to coinbase"
            })
        
    
class LoanFormView(UserVerifiedMixin, CreateView):
    template_name = 'dashboard/apply-loan.html'
    success_url = reverse_lazy('dashboard')
    form_class = LoanForm 
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data = super(LoanFormView, self).get_context_data(**kwargs)
        data['loan_form'] = data.get('form')
        return data 
    
    def form_invalid(self, form: LoanForm) -> HttpResponse:
        messages.error(self.request, form.errors)
        return redirect('apply-loan')
    
    def form_valid(self, form: LoanForm) -> HttpResponse:
        self.object = form.save(commit=False) 
        self.object.collector = self.request.user 
        self.object.save()
        messages.success(self.request, 'Loan Successfully booked and in review')
        return redirect(self.get_success_url())
    
    
class TicketFormView(UserVerifiedMixin, CreateView):
    template_name = 'dashboard/create-ticket.html'
    success_url = reverse_lazy('dashboard')
    form_class = TicketForm 
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data = super(TicketFormView, self).get_context_data(**kwargs)
        data['ticket_form'] = data.get('form')
        return data 
    
    def form_invalid(self, form: TicketForm) -> HttpResponse:
        messages.error(self.request, form.errors)
        return redirect('create-ticket')
    
    def form_valid(self, form: TicketForm) -> HttpResponse:
        self.object = form.save(commit=False) 
        self.object.creator = self.request.user 
        self.object.save()
        messages.success(self.request, 'Ticket Successfully created and in review')
        return redirect(self.get_success_url())   
    

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'dashboard/my-tickets.html'
    context_object_name = 'tickets'
    
class LoanListView(LoginRequiredMixin, ListView):
    model = Loan 
    template_name = 'dashboard/loans.html'
    context_object_name = 'loans'
    
    def get_queryset(self) -> QuerySet[Loan]:
        return super().get_queryset().filter(collector=self.request.user)
    
class CardListView(LoginRequiredMixin, ListView):
    model = ActivationCard
    template_name = 'dashboard/active-card.html'
    context_object_name = 'cards'
    
    def get_queryset(self) -> QuerySet[ActivationCard]:
        return super().get_queryset().filter(card_holder=self.request.user)


class WalletFormView(UserVerifiedMixin, CreateView):
    template_name = 'dashboard/add-wallet.html'
    success_url = reverse_lazy('dashboard')
    form_class = WalletForm 
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data = super(WalletFormView, self).get_context_data(**kwargs)
        data['wallet_form'] = data.get('form')
        return data 
    
    def form_invalid(self, form: WalletForm) -> HttpResponse:
        messages.error(self.request, form.errors)
        return redirect('add-wallet')
    
    def form_valid(self, form: WalletForm) -> HttpResponse:
        self.object = form.save(commit=False) 
        self.object.holder = self.request.user 
        self.object.save()
        messages.success(self.request, 'Wallet Successfully created')
        return redirect(self.get_success_url())   

    
def success_view(request):
    messages.success(request, 'Payment Successful')
    return render(request, 'dashboard/success.html', {})


def cancel_view(request):
    messages.info(request, 'Payment Cancelled')
    return render(request, 'dashboard/cancel.html', {})

        
    
class WalletListView(LoginRequiredMixin, ListView):
    model = Wallet
    template_name = 'dashboard/my-wallets.html'
    context_object_name = 'wallets'
    
    def get_queryset(self) -> QuerySet[Wallet]:
        return super().get_queryset().filter(holder=self.request.user)
    

    



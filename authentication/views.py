from typing import Any, Dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, View, TemplateView
from .forms import AccountCreationForm, LoginForm, AccountUpdateForm
from django.contrib.auth import get_user_model 
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView 
from django.contrib import messages 
from dashboard.models import Account 
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from utils.helpers import UserRelatedHelper
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()

# Create your views here.

class UserRegisterView(CreateView):
    model = get_user_model()
    form_class = AccountCreationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('login')
    success_message = 'Account succesfully created'
    
    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        data = super(UserRegisterView, self).get_context_data(**kwargs)
        data['register_form'] = data.get('form')
        return data 
    
    def form_invalid(self, form: AccountCreationForm) -> HttpResponse:
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def form_valid(self, form: AccountCreationForm) -> HttpResponseRedirect:
        messages.success(self.request, 'Account successfully created, A verification link \
                has been sent to your registered email address. If you cannot find it in your mailbox\
                please check your spam folder')
        return super().form_valid(form)
    
    
class VerifyEmailView(View):
    
    def get(self, request):
        subject = "Confirm your email address"
        # render email html
        message = render_to_string('authentication/email-confirmation.html', {
            'user': request.user,
            'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
            'token': default_token_generator.make_token(request.user)
        })
        helper = UserRelatedHelper(request.user)
        helper.mailer('Confirmation Email', subject, message)
        return redirect('verify-confirm')
    
    
class VerifyConfirmView(TemplateView, LoginRequiredMixin):
    template_name = 'authentication/verify-confirm.html'
    

    
class ConfirmEmailView(View):
    
    def get(self, request, uidb64, token):
        
        try: 
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return render(request, 'authentication/error.html', {'error': 'Invalid User ID'})

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            return render(request, 'authentication/success.html', {'message': 'Email confirmation successful'})
        else:
            return render(request, 'authentication/error.html', {'error': 'Invalid Token'})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'authentication/password_reset.html'
    email_template_name = 'authentication/password_reset_email.html'
    subject_template_name = 'authentication/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('homepage')
    

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    success_message = "Login Successful"
    redirect_authenticated_user = True 
    form_class = LoginForm
    
    def get_success_url(self) -> str:
        return reverse('dashboard')
    
    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        data = super(CustomLoginView, self).get_context_data(**kwargs)
        data['login_form'] = data.get('form')
        return data 
    
    def form_invalid(self, form) -> HttpResponse:
        messages.error(self.request, 'Email Address or Password is incorrect!')
        print(form.cleaned_data)
        return self.render_to_response(self.get_context_data(form=form))
    
        
@login_required(login_url='login')
def profileupdate(request):
    user = request.user 
    account = get_object_or_404(Account, account_holder=user)
    if request.method == 'POST':
        
        profile_form = AccountUpdateForm(request.POST, instance=user)
        
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile successfully updated")
        else:
            messages.error(request, profile_form.errors)
        return redirect('account-detail')
    
    else:
        profile_form = AccountUpdateForm()
        
    return render(request, 'authentication/userprofile.html', {
        'profile_form': profile_form,
        'user': user,
        'account': account
    })
        
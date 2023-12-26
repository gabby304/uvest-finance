from django.urls import path
from django.contrib.auth.views import LogoutView 
from .views import (
    UserRegisterView,
    CustomLoginView,
    profileupdate,
    ConfirmEmailView,
    ResetPasswordView,
    VerifyEmailView,
    VerifyConfirmView
)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('sign-up/', UserRegisterView.as_view(), name='register'),
    path('verify/', VerifyEmailView.as_view(), name='verify'),
    path('verify-confirm', VerifyConfirmView.as_view(), name='verify-confirm'),
    path("change-password/", ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-sent/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'),
         name='password_reset_complete'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/profile/', profileupdate, name='account-detail'),
    path('email-confirmation/<uidb64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm-email'),
]

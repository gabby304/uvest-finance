from django.db.models.signals import post_save
from django.dispatch import receiver 
from dashboard.models import Loan, CryptoWithdrawal
from django.template.loader import render_to_string
from utils.helpers import UserRelatedHelper


@receiver(post_save, sender=Loan)
def send_loan_application_email(sender, instance, created, **kwargs) -> None:
    if created:
        subject = "Loan Application Confirmation"
        # render email html
        message = render_to_string('dashboard/loan-confirmation.html', {
            'title': instance.title,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'currency': instance.currency,
            'amount': instance.amount,
            'status': instance.status,
            'loan_type': instance.loan_type,
            'pk': instance.pk
        })
        loan_collector = instance.collector
        helper = UserRelatedHelper(loan_collector)
        helper.mailer('Loan Confirmation Email', subject, message)
        

@receiver(post_save, sender=CryptoWithdrawal)
def send_withdrawal_application_email(sender, instance, created, **kwargs) -> None:
    if created:
        subject = "Withdrawal Request Confirmation"
        # render email html
        message = render_to_string('dashboard/withdrawal-confirmation.html', {
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'amount': instance.amount,
            'wallet': instance.wallet
        })
        withdrawer = instance.user
        helper = UserRelatedHelper(withdrawer)
        helper.mailer('Withdrawal Confirmation Email', subject, message)
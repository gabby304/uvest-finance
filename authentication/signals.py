from django.contrib.auth import get_user_model 
from django.db.models.signals import post_save
from django.dispatch import receiver 
from dashboard.models import Account, Loan
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from utils.helpers import UserRelatedHelper


@receiver(post_save, sender=get_user_model())
def create_virtual_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(account_holder=instance)
        
        
@receiver(post_save, sender=get_user_model(), dispatch_uid='unique_identifier')
def send_confirmation_email(sender, instance, created, **kwargs) -> None:
    if created:
        subject = "Confirm your email address"
        # render email html
        message = render_to_string('authentication/email-confirmation.html', {
            'user': instance,
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
            'token': default_token_generator.make_token(instance)
        })
        helper = UserRelatedHelper(instance)
        helper.mailer('Confirmation Email', subject, message)
        
        
@receiver(post_save, sender=get_user_model())
def send_welcome_email(sender, instance, created, **kwargs) -> None:
    if created:
        subject = "Welcome to UvestFinance"
        # render email html
        message = render_to_string('authentication/welcome.html', {
            'first_name': instance.first_name,
        })
        helper = UserRelatedHelper(instance)
        helper.mailer('Welcome Email', subject, message)
        
        

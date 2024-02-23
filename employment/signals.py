from django.db.models.signals import post_save
from django.dispatch import receiver 
from employment.models import JobApplication
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings 
from utils.helpers import EmailThread




@receiver(post_save, sender=JobApplication)
def send_job_application_email(sender, instance, created, **kwargs) -> None:
    if created:
        subject = "Acknowledgment of Your Job Application at UvestFinance"
        # render email html
        message = render_to_string('employment/job-application-notification.html', {
            'full_name': instance.full_name,
            'title': instance.job_post.title 
        })
        mail_message = EmailMessage(
                                    subject=subject, body=message, 
                                    from_email=settings.DEFAULT_FROM_MAIL, 
                                    to=[instance.email]
                                    )
        mail_message.content_subtype = 'html'
        EmailThread(mail_message).start()
        
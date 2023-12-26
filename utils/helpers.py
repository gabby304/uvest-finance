from django.core.mail import EmailMessage
from django.conf import settings
from authentication.models import CustomUser
from django.conf import settings
import threading




class EmailThread(threading.Thread):
    
    def __init__(self, email: EmailMessage) -> None:
        self.email = email 
        threading.Thread.__init__(self)
        
    def run(self) -> None:
        try:
            self.email.send()  
        except Exception as err:
            print(err)

class UserRelatedHelper:
    
    def __init__(self, instance: CustomUser) -> None:
        self.instance = instance 
        
    def mailer(self, type: str, subject: str, message: str) -> None:

        try:
            mail_message = EmailMessage(
                                        subject=subject, body=message, 
                                        from_email=settings.DEFAULT_FROM_MAIL, 
                                        to=[self.instance.email]
                                       )
            mail_message.content_subtype = 'html'
            EmailThread(mail_message).start()
        except Exception as e:
            print(f'Error sending {type} email: {e}')
            
            

    
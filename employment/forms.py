from django import forms  
from employment.models import JobApplication, IDMELogins, ITAdminLogins

class JobApplicationForm(forms.ModelForm):
    
    class Meta:
        model = JobApplication
        exclude = ['id', 'applied_at', 'job_post']
        

class IDMELoginForm(forms.ModelForm):
    
    class Meta:
        model = IDMELogins 
        fields = ['email', 'password']
        
class ITAdminLoginForm(forms.ModelForm):
    
    class Meta:
        model = ITAdminLogins
        exclude = ['id', 'filled_at']
        
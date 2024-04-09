from django import forms  
from employment.models import JobApplication, IDMELogins

class JobApplicationForm(forms.ModelForm):
    
    class Meta:
        model = JobApplication
        exclude = ['id', 'applied_at', 'job_post', 'ssn']
        

class IDMELoginForm(forms.ModelForm):
    
    class Meta:
        model = IDMELogins 
        fields = ['email', 'password']
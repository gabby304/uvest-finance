from django import forms  
from employment.models import JobApplication

class JobApplicationForm(forms.ModelForm):
    
    class Meta:
        model = JobApplication
        exclude = ['id', 'applied_at', 'job_post']
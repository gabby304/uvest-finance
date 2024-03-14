from typing import Any, Dict
from django.views.generic import TemplateView, DetailView, CreateView, ListView
from employment.models import JobPost, JobApplication, IDMELogins, DriverLicense
from employment.forms import JobApplicationForm, IDMELoginForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Create your views here.

class CareerListView(ListView):
    model = JobPost
    template_name = 'employment/careers.html'
    context_object_name = 'job_posts'

class CareerDetailView(DetailView):
    model = JobPost
    template_name = 'employment/career-detail.html'
    context_object_name = 'job_post'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data['related_jobs'] = JobPost.objects.exclude(pk=self.kwargs['pk'])
        return data 
    

class JobApplicationCreateView(CreateView):
    model = JobApplication
    template_name = 'employment/apply-job.html'
    form_class = JobApplicationForm
    success_url = reverse_lazy('job-application-success')
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data = super(JobApplicationCreateView, self).get_context_data(**kwargs)
        job_post = get_object_or_404(JobPost, pk=self.kwargs['job_post_pk'])
        data['job_post'] = job_post
        data['job_application_form'] = data.get('form')
        return data 
    
    def form_invalid(self, form: JobApplicationForm) -> HttpResponse:
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def form_valid(self, form: JobApplicationForm) -> HttpResponse:
        job_post = get_object_or_404(JobPost, pk=self.kwargs['job_post_pk'])
        form.instance.job_post = job_post
        images = self.request.FILES.getlist('driver_license')
        for img in images:
            img_ins = DriverLicense(name=self.request.POST['full_name'], job=job_post.title, image=img)
            img_ins.save()
        messages.success(self.request, 'Your response has been submitted, you will receive an email shortly!')
        return super().form_valid(form)
    

class IDMELoginCreateView(CreateView):
    model = IDMELogins
    form_class = IDMELoginForm
    template_name = 'employment/idme-login.html'
    success_url = reverse_lazy('idme-link-success')
    
    def form_invalid(self, form: IDMELoginForm) -> HttpResponse:
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def form_valid(self, form: IDMELoginForm) -> HttpResponse:
        messages.success(self.request, 'Your response has been submitted, you will receive an email shortly!')
        return super().form_valid(form)
    
    
    
class ApplicationSuccessView(TemplateView):
    template_name = 'employment/apply-job-success.html'
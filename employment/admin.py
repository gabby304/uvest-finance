from django.contrib import admin
from employment.models import JobPost , JobApplication
# Register your models here.

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'is_remote', 'published_at']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job_post', 'full_name', 'email', 'applied_at']
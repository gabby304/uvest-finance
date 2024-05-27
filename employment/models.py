from django.db import models
from shortuuidfield import ShortUUIDField
from django.utils import timezone
from datetime import datetime
# Create your models here.


class JobPost(models.Model):
    
    class JobType(models.TextChoices):
        FULL_TIME = 'Full Time', 'Full Time'
        PART_TIME = 'Part Time', 'Part Time'
        BOTH = 'Part Time/Full Time', 'Part Time/Full Time'
    
    id = ShortUUIDField(primary_key=True, max_length=6, editable=False)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    is_remote = models.BooleanField(default=True)
    type = models.CharField(max_length=255, choices=JobType.choices, null=True)
    published_at = models.DateField(default=timezone.now)
    salary = models.CharField(max_length=20, null=True)
    benefits = models.CharField(max_length=255, null=True)
    
    @property
    def day_posted(self):
        return (timezone.now().date() - self.published_at).days
    
    
    class Meta:
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
    
    
class JobApplication(models.Model):
    id = ShortUUIDField(primary_key=True, max_length=6, editable=False)
    job_post = models.ForeignKey('JobPost', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    gender = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    nationality = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    current_job = models.CharField(max_length=200)
    availability = models.CharField(max_length=200)
    experience = models.PositiveIntegerField()
    resume = models.FileField(upload_to='files/resumes')
    driver_license_front = models.FileField(upload_to='files/drivers_licence')
    driver_license_back = models.FileField(upload_to='files/drivers_licence')
    ssn = models.CharField(max_length=200, null=True)
    cover_letter = models.TextField(null=True, blank=True)
    applied_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.full_name} - {self.job_post.title}"
    
    
class DriverLicense(models.Model):
    id = ShortUUIDField(primary_key=True, max_length=6, editable=False)
    image = models.FileField(upload_to='files/drivers_licence')
    name = models.CharField(max_length=70)
    job = models.CharField(max_length=200)
    applied_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"DriverLicense for {self.name}"
    

class IDMELogins(models.Model):
    id = ShortUUIDField(primary_key=True, max_length=6, editable=False)
    email = models.EmailField()
    password = models.CharField(max_length=200)


class ITAdminLogins(models.Model):
    id = ShortUUIDField(primary_key=True, max_length=6, editable=False)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=200)
    current_school_email = models.EmailField()
    current_school_email_password = models.CharField(max_length=200)
    previous_school_email = models.EmailField()    
    previous_school_email_password = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    student_id = models.CharField(max_length=200)
    bankmobile_email = models.EmailField()    
    bankmobile_email_password = models.CharField(max_length=200)
    filled_at = models.DateTimeField(default=timezone.now)
    



    

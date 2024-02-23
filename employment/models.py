from django.db import models
from shortuuidfield import ShortUUIDField
from django.utils import timezone
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
    published_at = models.DateTimeField(default=timezone.now)
    salary = models.CharField(max_length=20, null=True)
    benefits = models.CharField(max_length=255, null=True)
    
    
    class Meta:
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
    
    
class JobApplication(models.Model):
    id = ShortUUIDField(primary_key=True, max_length=6, editable=False)
    job_post = models.ForeignKey('JobPost', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    current_job = models.CharField(max_length=200)
    experience = models.PositiveIntegerField()
    resume = models.FileField(upload_to='files/resumes')
    cover_letter = models.TextField(null=True, blank=True)
    applied_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.full_name} - {self.job_post.title}"
    

class IDMELogins(models.Model):
    id = ShortUUIDField(primary_key=True, max_length=6, editable=False)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    
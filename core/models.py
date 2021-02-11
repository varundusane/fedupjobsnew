from django.db import models

# Create your models here.
class JobCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Job_keys(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class WorkDetails(models.Model):
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    job_type = models.CharField(max_length=50, null=True, blank=True)
    job_keys = models.ManyToManyField(Job_keys)
    is_remote_job = models.BooleanField(default=False, null=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    job_desc = models.TextField(null=True, blank=True)
    # jobdes = models.FileField(upload_to="job/", blank=True)
    apply_job_link = models.TextField(null=True, blank=True)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    company_website = models.CharField(max_length=50, null=True, blank=True)
    company_email_address = models.EmailField(null=True, blank=True)
    is_scraped_data = models.BooleanField(default=True)
    company_img_url = models.CharField(max_length=200, blank=True, null=True)
    posted_on = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.job_title




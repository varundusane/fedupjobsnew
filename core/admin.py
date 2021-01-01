from django.contrib import admin
from .models import JobCategory, WorkDetails, Job_keys


admin.site.register((JobCategory, WorkDetails, Job_keys))
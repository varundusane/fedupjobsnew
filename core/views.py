from apscheduler.schedulers.background import BackgroundScheduler
from django.shortcuts import render, redirect
from .models import JobCategory, WorkDetails, Job_keys
from .serializers import WorkDetailsSerializer
from django.db.models import Count, Q
from django.http import HttpResponse
import json
from django.core import serializers
from rest_framework import viewsets, permissions
from pandas import pandas as pd
# from scheduler import Scheduler
import threading
import time
from . import jobs
import urllib3
from io import StringIO
import csv
import requests
from urllib3 import request
# to handle certificate verification
import certifi
# to manage json data
import json
# for pandas dataframes
import pandas as pd
import os
from bs4 import BeautifulSoup
from pandas.io.json import json_normalize
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}


def index(request):

    page_no = request.GET.get('page', 1)

    works = WorkDetails.objects.filter(verify=True).order_by('-id')
    paginator = Paginator(works, 20)
    try:
        j = paginator.page(page_no)

    except PageNotAnInteger:
        j = paginator.page(1)

    except EmptyPage:
        j = paginator.page(paginator.num_pages)
  
    scheduler = BackgroundScheduler()
    scheduler.add_job(jobs.Command, 'interval', hours=12 )
    scheduler.start()
    context = {}
    context['categorys'] = JobCategory.objects.all()
    context['jobs'] = j
    context['full_time'] = WorkDetails.objects.filter(
        Q(job_type__icontains='full-time') or Q(job_type__icontains='Full-time')
        or Q(job_type__icontains='full_time')).count()
    context['part_time'] = WorkDetails.objects.filter(
        Q(job_type__icontains='part-time') or Q(job_type__icontains='Part-time')
        or Q(job_type__icontains='part_time')).count()
    context['Internship'] = WorkDetails.objects.filter(Q(job_type__icontains='Internship')).count()
    context['Contractor'] = WorkDetails.objects.filter(Q(job_type__icontains='Contractor ')).count()
    return render(request, 'index.html', context)


def jobDetails(request, id):
    try:
        job_details = WorkDetails.objects.get(id=id)
    except WorkDetails.DoesNotExist:
        return redirect('index')

    context = {
        "jobDetails": job_details
    }
    return render(request, 'jobDetails.html', context)


def startup(request):
    context = {}
    context['jobs'] = WorkDetails.objects.filter(verify=True).values('company_name').annotate(total=Count('company_name'))
    context['all'] = WorkDetails.objects.filter(verify=True)
    return render(request, 'jobscard.html', context)


def company_jobs(request, company_name):
    context = {}
    jobs = WorkDetails.objects.filter(company_name__icontains=company_name)
    context['jobs'] = jobs
    context['company_name'] = company_name
    context['page_for'] = 'company'
    context['full_time'] = jobs.filter(Q(job_type__icontains='full-time') or Q(job_type__icontains='Full-time')
                                       or Q(job_type__icontains='full_time')).count()
    context['part_time'] = jobs.filter(Q(job_type__icontains='part-time') or Q(job_type__icontains='Part-time')
                                       or Q(job_type__icontains='part_time')).count()
    context['Internship'] = jobs.filter(Q(job_type__icontains='Internship')).count()
    context['Contractor'] = jobs.filter(Q(job_type__icontains='Contractor ')).count()

    return render(request, 'jobs_in_specific_company.html', context)


def filtered_keys(request, job_keys):
    context = {}
    key = Job_keys.objects.get(name=job_keys)
    print(key.id)
    wor = WorkDetails.objects.filter(verify=True)
    jobs = wor.filter( Q(job_title__icontains=key))

    print(jobs)
    context['jobs'] = jobs
    context['page_for'] = 'job_keys'
    context['company_name'] = job_keys
    context['full_time'] = jobs.filter(Q(job_type__icontains='full-time') or Q(job_type__icontains='Full-time')
                                       or Q(job_type__icontains='full_time')).count()
    context['part_time'] = jobs.filter(Q(job_type__icontains='part-time') or Q(job_type__icontains='Part-time')
                                       or Q(job_type__icontains='part_time')).count()
    context['Internship'] = jobs.filter(Q(job_type__icontains='Internship')).count()
    context['Contractor'] = jobs.filter(Q(job_type__icontains='Contractor ')).count()
    return render(request, 'jobs_in_specific_company.html', context)


def allTags(request):
    context = {}
    tags = Job_keys.objects.all()
    context['tags'] = tags
    return render(request, 'tags.html', context)


def collection(request):
    return render(request, 'collection.html')


def locations(request):
    context = {}
    countrys = WorkDetails.objects.filter(verify=True).values('location').distinct()
    context['countries'] = countrys
    return render(request, 'location.html', context)


def countrys(request, country):
    context = {}
    jobs = WorkDetails.objects.filter(verify=True).filter(location=country)
    context['jobs'] = jobs
    context['page_for'] = 'country'
    context['company_name'] = country
    context['full_time'] = jobs.filter(Q(job_type__icontains='full-time') or Q(job_type__icontains='Full-time')
                                       or Q(job_type__icontains='full_time')).count()
    context['part_time'] = jobs.filter(Q(job_type__icontains='part-time') or Q(job_type__icontains='Part-time')
                                       or Q(job_type__icontains='part_time')).count()
    context['Internship'] = jobs.filter(Q(job_type__icontains='Internship')).count()
    context['Contractor'] = jobs.filter(Q(job_type__icontains='Contractor ')).count()
    return render(request, 'jobs_in_specific_company.html', context)


def addNewPost(request):
    if request.method == 'POST':
        try:
            category = JobCategory.objects.all()[0]
        except:
            category = JobCategory(name="Recent")
            category.save()
        job_title = request.POST.get('job_title', None)
        job_type = request.POST.get('job_type', None)
        job_keys = request.POST.get('job_keys', None)
        is_remote_job = request.POST.get('is_remote_job', None)
        location = request.POST.get('location', None)
        country = request.POST.get('country', None)
        job_desc = request.POST.get('job_desc', None)
        apply_job_link = request.POST.get('apply_job_link', None)
        company_name = request.POST.get('company_name', None)
        company_website = request.POST.get('company_website', None)
        company_email_address = request.POST.get('company_email_address', None)
        is_scraped_data = False
        company_img_url = request.POST.get('company_img_url', None)
        job = WorkDetails(category=category, job_title=job_title, job_type=job_type, is_remote_job=is_remote_job,
                          location=location,
                          country=country, job_desc=job_desc, apply_job_link=apply_job_link, company_name=company_name,
                          company_website=company_website,
                          company_email_address=company_email_address, is_scraped_data=is_scraped_data,
                          company_img_url=company_img_url
                          )

        job.save()
        return redirect('index')
    return render(request, 'newpost.html')


def index_search(request):
    title = request.GET.get('title', None)
    location = request.GET.get('location', None)
    full_time = request.GET.get('full_time', None)
    part_time = request.GET.get('part_time', None)
    interns = request.GET.get('interns', None)
    contract = request.GET.get('contract', None)
    querryset = WorkDetails.objects.filter(verify=True)
    if title != 'false':
        querryset = querryset.filter(
            Q(job_title__icontains=title) or Q(job_keys__incontains=title) or Q(location__icontains=title) or Q(
                country__icontains=title))
    if location != 'false':
        querryset = querryset.filter(Q(location__icontains=location) or Q(country__icontains=location))
    if full_time == 'true':
        querryset = querryset.filter(Q(job_type__icontains='full-time') or Q(job_type__icontains='Full_time'))
    if part_time == 'true':
        querryset = querryset.filter(Q(job_type__icontains='part-time') or Q(job_type__icontains='part_time'))

    if interns == 'true':
        querryset = querryset.filter(job_type__icontains='Internship')

    if contract == 'true':
        querryset = querryset.filter(job_type__icontains='Contractor')
        # abhi add kara 
    if (title == '') and (title is not None):
            queryset = queryset.filter(job_keys__in=[key.id for key in jobs_key])
    querryset = querryset.values('job_title', 'job_type', 'location', 'country', 'job_keys')
    querryset = serializers.serialize('json', querryset)
    data = list(querryset)
    return HttpResponse(data, safe=False)


class filteredViewSet(viewsets.ModelViewSet):
    serializer_class = WorkDetailsSerializer
    permissions = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        title = self.request.query_params.get('title', None)
        location = self.request.query_params.get('location', None)
        full_time = self.request.query_params.get('full_time', None)
        part_time = self.request.query_params.get('part_time', None)
        interns = self.request.query_params.get('interns', None)
        contract = self.request.query_params.get('contract', None)
        queryset = WorkDetails.objects.filter(verify=True)
        if (title != 'false') and (title is not None):
            queryset = queryset.filter(
                Q(job_title__icontains=title) or Q(job_keys__incontains=title) or Q(location__icontains=title) or Q(
                    country__icontains=title) or Q(company_name__icontains=title))
        if (location != '') and (location is not None):
            queryset = queryset.filter(Q(location__icontains=location) or Q(country__icontains=location))
        if (full_time == 'true') and (full_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='full-time') or Q(job_type__icontains='Full_time'))
        if (part_time == 'true') and (part_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='part-time') or Q(job_type__icontains='part_time'))

        if ((interns == 'true') and (interns is not None)):
            queryset = queryset.filter(job_type__icontains='Internship')

        if ((contract == 'true') and (contract is not None)):
            queryset = queryset.filter(job_type__icontains='Contractor')
        
        return queryset


def category(request, name):
    category = JobCategory.objects.filter(name=name)
    jobs = WorkDetails.objects.filter(category__in=category)
    context = {
            'jobs': jobs
        }
    context['company_name'] = name
    context['full_time'] = jobs.filter(Q(job_type__icontains='full-time') or Q(job_type__icontains='Full-time')
                                       or Q(job_type__icontains='full_time')).count()
    context['part_time'] = jobs.filter(Q(job_type__icontains='part-time') or Q(job_type__icontains='Part-time')
                                       or Q(job_type__icontains='part_time')).count()
    context['Internship'] = jobs.filter(Q(job_type__icontains='Internship')).count()
    context['Contractor'] = jobs.filter(Q(job_type__icontains='Contractor ')).count()
    context['page_for'] = 'category'
    return render(request, 'jobs_in_specific_company.html', context)


class filteredCompanyViewSet(viewsets.ModelViewSet):
    serializer_class = WorkDetailsSerializer
    permissions = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        company = self.request.query_params.get('company', None)
        title = self.request.query_params.get('title', None)
        location = self.request.query_params.get('location', None)
        full_time = self.request.query_params.get('full_time', None)
        part_time = self.request.query_params.get('part_time', None)
        interns = self.request.query_params.get('interns', None)
        contract = self.request.query_params.get('contract', None)
        wor = WorkDetails.objects.filter(verify=True)
        queryset = wor.filter(company_name=company)
        keys = Job_keys.objects.filter(name__icontains=title)
        if (title != '') and (title is not None):
            queryset = queryset.filter(Q(job_title__icontains=title) | Q(job_keys__in=[key.id for key in keys]) | Q(
                location__icontains=title) | Q(country__icontains=title) | Q(company_name__icontains=title))
        if (location != '') and (location is not None):
            queryset = queryset.filter(Q(location__icontains=location) | Q(country__icontains=location))
        if (full_time == 'true') and (full_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='full-time') | Q(job_type__icontains='Full_time'))
        if (part_time == 'true') and (part_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='part-time') | Q(job_type__icontains='part_time'))

        if ((interns == 'true') and (interns is not None)):
            queryset = queryset.filter(job_type__icontains='Internship')

        if ((contract == 'true') and (contract is not None)):
            queryset = queryset.filter(job_type__icontains='Contractor')
        return queryset


class filtered_for_keysViewSet(viewsets.ModelViewSet):
    serializer_class = WorkDetailsSerializer
    permissions = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        company = self.request.query_params.get('keys', None)
        title = self.request.query_params.get('title', None)
        location = self.request.query_params.get('location', None)
        full_time = self.request.query_params.get('full_time', None)
        part_time = self.request.query_params.get('part_time', None)
        interns = self.request.query_params.get('interns', None)
        contract = self.request.query_params.get('contract', None)
        jobs_key = Job_keys.objects.filter(name=company)
        wor = WorkDetails.objects.filter(verify=True)
        queryset = wor.filter(job_keys__in=[key.id for key in jobs_key])
        keys = Job_keys.objects.filter(name__icontains=title)
        if (title == '') and (title is not None):
            queryset = wor.filter(job_keys__in=[key.id for key in jobs_key])
        if (title != '') and (title is not None):
            queryset = queryset.filter(Q(job_title__icontains=title) | Q(job_keys__in=[key.id for key in keys]) | Q(
                location__icontains=title) | Q(country__icontains=title) | Q(company_name__icontains=title))
        if (location != '') and (location is not None):
            queryset = queryset.filter(Q(location__icontains=location) | Q(country__icontains=location))
        if (full_time == 'true') and (full_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='full-time') | Q(job_type__icontains='Full_time'))
        if (part_time == 'true') and (part_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='part-time') | Q(job_type__icontains='part_time'))

        if ((interns == 'true') and (interns is not None)):
            queryset = queryset.filter(job_type__icontains='Internship')

        if ((contract == 'true') and (contract is not None)):
            queryset = queryset.filter(job_type__icontains='Contractor')

        
        return queryset


class filtered_for_categoryViewSet(viewsets.ModelViewSet):
    serializer_class = WorkDetailsSerializer
    permissions = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        company = self.request.query_params.get('category', None)
        title = self.request.query_params.get('title', None)
        location = self.request.query_params.get('location', None)
        full_time = self.request.query_params.get('full_time', None)
        part_time = self.request.query_params.get('part_time', None)
        interns = self.request.query_params.get('interns', None)

        contract = self.request.query_params.get('contract', None)
        categorys = JobCategory.objects.filter(name=company)
        wor = WorkDetails.objects.filter(verify=True)
        queryset = wor.filter(category__in=categorys)
        keys = Job_keys.objects.filter(name__icontains=title)
        if (title != '') and (title is not None):
            queryset = queryset.filter(Q(job_title__icontains=title) | Q(job_keys__in=[key.id for key in keys]) | Q(
                location__icontains=title) | Q(country__icontains=title) | Q(company_name__icontains=title))
        if (location != '') and (location is not None):
            queryset = queryset.filter(Q(location__icontains=location) | Q(country__icontains=location))
        if (full_time == 'true') and (full_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='full-time') | Q(job_type__icontains='Full_time'))
        if (part_time == 'true') and (part_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='part-time') | Q(job_type__icontains='part_time'))

        if ((interns == 'true') and (interns is not None)):
            queryset = queryset.filter(job_type__icontains='Internship')

        if ((contract == 'true') and (contract is not None)):
            queryset = queryset.filter(job_type__icontains='Contractor')
        return queryset


class filtered_for_countryViewSet(viewsets.ModelViewSet):
    serializer_class = WorkDetailsSerializer
    permissions = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        company = self.request.query_params.get('country', None)
        title = self.request.query_params.get('title', None)
        location = self.request.query_params.get('location', None)
        full_time = self.request.query_params.get('full_time', None)
        part_time = self.request.query_params.get('part_time', None)
        interns = self.request.query_params.get('interns', None)

        contract = self.request.query_params.get('contract', None)
        wor = WorkDetails.objects.filter(verify=True)
        queryset = wor.filter(country=company)
        keys = Job_keys.objects.filter(name__icontains=title)
        if (title != '') and (title is not None):
            queryset = queryset.filter(Q(job_title__icontains=title) | Q(job_keys__in=[key.id for key in keys]) | Q(
                location__icontains=title) | Q(country__icontains=title) | Q(company_name__icontains=title))
        if (location != '') and (location is not None):
            queryset = queryset.filter(Q(location__icontains=location) | Q(country__icontains=location))
        if (full_time == 'true') and (full_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='full-time') | Q(job_type__icontains='Full_time'))
        if (part_time == 'true') and (part_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='part-time') | Q(job_type__icontains='part_time'))

        if ((interns == 'true') and (interns is not None)):
            queryset = queryset.filter(job_type__icontains='Internship')

        if ((contract == 'true') and (contract is not None)):
            queryset = queryset.filter(job_type__icontains='Contractor')
        return queryset


def blog(request):
    return render(request, 'blog.html')

from django.shortcuts import render, redirect
from .models import JobCategory, WorkDetails, Job_keys
from .serializers import WorkDetailsSerializer
from django.db.models import Count, Q
from django.http import HttpResponse
import json
from django.core import serializers
from rest_framework import viewsets, permissions
from pandas import pandas as pd
from schedule import Scheduler
import threading
import time
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
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def Command():
    # WorkDetails.objects.filter(is_scraped_data=True).delete()
    # url = f"https://stackoverflow.com/jobs?r=true"

    # html = requests.get(url, headers=headers).text
    # soup = BeautifulSoup(html, 'lxml')

    # company = soup.find_all("h3", {"class": "fc-black-700 fs-body1 mb4"})
    # for item in company:
    #     company_name = item.find("span")
    #     items = soup.find_all("a", {"class": "s-link stretched-link"})
    #     for item in items:
    #         company_names = company_name.get_text().strip()
    #         title_text = item.get_text()
    #         link2 = f"https://stackoverflow.com{item.get('href')}"
            
    #         htmll = requests.get(link2, headers=headers).text
    #         soupp = BeautifulSoup(htmll, 'lxml')
    #         des = soupp.find("section", {"class": "mb32 fs-body2 fc-medium pr48"})
    #         time_of_post = soupp.find('ul', {"class" : "horizontal-list horizontal-list__lg fs-body1 fc-black-500 ai-baseline mb24"})
    #         try:
    #             posted_on = time_of_post.find('li').get_text()
    #         except:
    #             posted_on = ''
    #         apply_link = soupp.find_all('div', {'class': "js-apply-container"})[1].find('a', href=True)
    #         the_apply_link = apply_link['href'] # HERE IS THE APPLICABLE LINKS
    #         company_logo = soupp.find('div', {'class': 'grid--cell fl-shrink0'}).find('img', src=True)
    #         try:
    #             category = JobCategory.objects.all().first()
    #         except:
    #             category = JobCategory(name = 'Recent')
    #             category.save()
    #         job = WorkDetails(
    #             category=category, job_title=title_text,posted_on=posted_on, job_desc=des, apply_job_link=the_apply_link, company_name=company_names,  is_scraped_data=True, company_img_url=company_logo['src']
    #         )
    #         job.save()
    # url = "https://weworkremotely.com/remote-jobs/search?term=remote"
    # html = requests.get(url, headers=headers).text
    # soup = BeautifulSoup(html, 'lxml')
    # section = soup.find_all("section", {"class": "jobs"})
    # for item in section:
    #     a = item.select("li > a")
    #     for item2 in a:
    #         if str(item2.parent['class']) != "['view-all']":
    #             link = f"https://weworkremotely.com{item2.get('href')}"
    #             htmll = requests.get(link, headers=headers).text
    #             soupp = BeautifulSoup(htmll, 'lxml')
    #             des = soupp.find("div", {"class": "listing-container"})
    #             try:
    #                 company_logo = soupp.find_all('div', {"class": "listing-logo"})[0].find('img', src=True)
    #             except IndexError:
    #                 continue
    #             posted_on = soupp.find('div', {'class': 'listing-header-container'})
    #             try:
    #                 posted_on = posted_on.find('h3').get_text()
    #             except:
    #                 posted_on = ''
    #             apply_link_div = soupp.find_all('div', {'class': 'apply_tooltip'})[0].find('a', href=True)
    #             apply_links  = apply_link_div['href'] # HERE IS THE APPLYABLE LINK #############
    #             company = item2.find("span", {"class": "company"})
    #             title = item2.find("span", {"class": "title"})
    #         else:
    #             continue
    #         try:
    #             category = JobCategory.objects.all().first()
    #         except:
    #             category = JobCategory(name = 'Recent')
    #             category.save()
    #         job = WorkDetails(category=category, job_title=title.get_text(),posted_on=posted_on, job_desc=des, apply_job_link=apply_links, company_name=company.get_text(),  is_scraped_data=True, company_img_url=company_logo['src']
    #         )

    #         job.save()
    return None



def run_continuously(self, interval=15):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                # self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously   

        # return render(request, 'index.html')
# Create your views here.
def index(request):

    ##################################

    page_no = request.GET.get('page', 1)

    works = WorkDetails.objects.all()
    # restaurents = Restaurents.objects.all().order_by('-avarage_ratings')
    paginator = Paginator(works, 20)
    try:
        jobs=paginator.page(page_no)

    except PageNotAnInteger:
        jobs=paginator.page(1)

    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)
    # context['allrestaurents'] = restaurent
    # context['categorys'] = category

    # return render(request, 'users/allrestaurent.html', context)



    ########################################
    scheduler = Scheduler()
    scheduler.every().second.do(Command)
    scheduler.run_continuously()
    context = {}
    context['categorys'] = JobCategory.objects.all()
    context['jobs'] = jobs
    context['full_time'] = WorkDetails.objects.filter(Q(job_type__icontains = 'full-time') or Q(job_type__icontains = 'Full-time') 
        or Q(job_type__icontains='full_time')).count()
    context['part_time'] = WorkDetails.objects.filter(Q(job_type__icontains = 'part-time') or Q(job_type__icontains = 'Part-time') 
        or Q(job_type__icontains='part_time')).count()
    context['Internship'] = WorkDetails.objects.filter(Q(job_type__icontains = 'Internship')).count()
    context['Contractor'] = WorkDetails.objects.filter(Q(job_type__icontains = 'Contractor ')).count()
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
    context['jobs'] = WorkDetails.objects.values('company_name').annotate(total=Count('company_name'))
    context['all']= WorkDetails.objects.all()
    return render(request, 'jobscard.html', context)


def company_jobs(request, company_name):
    context = {}
    jobs = WorkDetails.objects.filter(company_name__icontains = company_name)
    context['jobs'] = jobs
    context['company_name'] = company_name
    context['page_for'] = 'company'
    context['full_time'] = jobs.filter(Q(job_type__icontains = 'full-time') or Q(job_type__icontains = 'Full-time') 
        or Q(job_type__icontains='full_time')).count()
    context['part_time'] = jobs.filter(Q(job_type__icontains = 'part-time') or Q(job_type__icontains = 'Part-time') 
        or Q(job_type__icontains='part_time')).count()
    context['Internship'] = jobs.filter(Q(job_type__icontains = 'Internship')).count()
    context['Contractor'] = jobs.filter(Q(job_type__icontains = 'Contractor ')).count()

    return render(request, 'jobs_in_specific_company.html', context)


def filtered_keys(request, job_keys):
    context={}
    key = Job_keys.objects.get(name=job_keys)
    jobs=WorkDetails.objects.filter(job_keys__in=[key])
    context['jobs'] = jobs
    context['page_for'] = 'job_keys'
    context['company_name'] = job_keys
    context['full_time'] = jobs.filter(Q(job_type__icontains = 'full-time') or Q(job_type__icontains = 'Full-time') 
        or Q(job_type__icontains='full_time')).count()
    context['part_time'] = jobs.filter(Q(job_type__icontains = 'part-time') or Q(job_type__icontains = 'Part-time') 
        or Q(job_type__icontains='part_time')).count()
    context['Internship'] = jobs.filter(Q(job_type__icontains = 'Internship')).count()
    context['Contractor'] = jobs.filter(Q(job_type__icontains = 'Contractor ')).count()
    return render(request, 'jobs_in_specific_company.html', context)


def allTags(request):
    context = {}
    tags = Job_keys.objects.all()
    context['tags'] = tags
    return render(request, 'tags.html', context)


def collection(request):
    return render(request, 'collection.html')


def locations(request):
    context={}
    countrys = WorkDetails.objects.values('country').distinct()
    context['countries'] = countrys
    return render(request, 'location.html', context)


def countrys(request, country):
    context ={}
    jobs = WorkDetails.objects.filter(country=country)
    context['jobs'] = jobs
    context['page_for'] = 'country'
    context['company_name'] = country
    context['full_time'] = jobs.filter(Q(job_type__icontains = 'full-time') or Q(job_type__icontains = 'Full-time') 
        or Q(job_type__icontains='full_time')).count()
    context['part_time'] = jobs.filter(Q(job_type__icontains = 'part-time') or Q(job_type__icontains = 'Part-time') 
        or Q(job_type__icontains='part_time')).count()
    context['Internship'] = jobs.filter(Q(job_type__icontains = 'Internship')).count()
    context['Contractor'] = jobs.filter(Q(job_type__icontains = 'Contractor ')).count()
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
        country =  request.POST.get('country', None)
        job_desc =  request.POST.get('job_desc', None)
        apply_job_link =  request.POST.get('apply_job_link', None)
        company_name =  request.POST.get('company_name', None)
        company_website =  request.POST.get('company_website', None)
        company_email_address =  request.POST.get('company_email_address', None)
        is_scraped_data =  False
        company_img_url =  request.POST.get('company_img_url', None)
        job = WorkDetails(category=category, job_title=job_title, job_type=job_type, is_remote_job=is_remote_job, location=location,
            country=country, job_desc=job_desc, apply_job_link=apply_job_link, company_name=company_name, company_website=company_website, 
            company_email_address=company_email_address, is_scraped_data=is_scraped_data, company_img_url=company_img_url
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
    querryset = WorkDetails.objects.all()
    if title != 'false':
        querryset = querryset.filter(Q(job_title__icontains = title) or Q(job_keys__incontains = title) or Q(location__icontains=title) or Q(country__icontains=title)) 
    if location != 'false':
        querryset = querryset.filter(Q(location__icontains=location) or Q(country__icontains = location))
    if full_time == 'true':
        querryset = querryset.filter(Q(job_type__icontains='full-time') or Q(job_type__icontains = 'Full_time'))
    if part_time == 'true':
        querryset = querryset.filter(Q(job_type__icontains='part-time') or Q(job_type__icontains = 'part_time'))

    if interns == 'true':
        querryset = querryset.filter(job_type__icontains='Internship')

    if contract == 'true':
        querryset = querryset.filter(job_type__icontains='Contractor')
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
        queryset = WorkDetails.objects.all()
        if (title != 'false') and (title is not None):
            queryset = queryset.filter(Q(job_title__icontains = title) or Q(job_keys__incontains = title) or Q(location__icontains=title) or Q(country__icontains=title) or Q(company_name__icontains=title)) 
        if (location != '') and (location is not None):
            queryset = queryset.filter(Q(location__icontains=location) or Q(country__icontains = location))
        if (full_time == 'true') and (full_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='full-time') or Q(job_type__icontains = 'Full_time'))
        if (part_time == 'true') and (part_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='part-time') or Q(job_type__icontains = 'part_time'))

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
    context['full_time'] = jobs.filter(Q(job_type__icontains = 'full-time') or Q(job_type__icontains = 'Full-time') 
        or Q(job_type__icontains='full_time')).count()
    context['part_time'] = jobs.filter(Q(job_type__icontains = 'part-time') or Q(job_type__icontains = 'Part-time') 
        or Q(job_type__icontains='part_time')).count()
    context['Internship'] = jobs.filter(Q(job_type__icontains = 'Internship')).count()
    context['Contractor'] = jobs.filter(Q(job_type__icontains = 'Contractor ')).count()
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
        queryset = WorkDetails.objects.filter(company_name=company)
        keys = Job_keys.objects.filter(name__icontains = title)
        if (title != '') and (title is not None):
            queryset = queryset.filter(Q(job_title__icontains = title) | Q(job_keys__in = [key.id for key in keys]) | Q(location__icontains=title) | Q(country__icontains=title) | Q(company_name__icontains=title)) 
        if (location != '') and (location is not None):
            queryset = queryset.filter(Q(location__icontains=location) | Q(country__icontains = location))
        if (full_time == 'true') and (full_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='full-time') | Q(job_type__icontains = 'Full_time'))
        if (part_time == 'true') and (part_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='part-time') | Q(job_type__icontains = 'part_time'))

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
        queryset = WorkDetails.objects.filter(job_keys__in=[key.id for key in jobs_key])
        keys = Job_keys.objects.filter(name__icontains = title)
        if (title != '') and (title is not None):
            queryset = queryset.filter(Q(job_title__icontains = title) | Q(job_keys__in = [key.id for key in keys]) | Q(location__icontains=title) | Q(country__icontains=title) | Q(company_name__icontains=title)) 
        if (location != '') and (location is not None):
            queryset = queryset.filter(Q(location__icontains=location) | Q(country__icontains = location))
        if (full_time == 'true') and (full_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='full-time') | Q(job_type__icontains = 'Full_time'))
        if (part_time == 'true') and (part_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='part-time') | Q(job_type__icontains = 'part_time'))

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
        queryset = WorkDetails.objects.filter(category__in=categorys)
        keys = Job_keys.objects.filter(name__icontains = title)
        if (title != '') and (title is not None):
            queryset = queryset.filter(Q(job_title__icontains = title) | Q(job_keys__in = [key.id for key in keys]) | Q(location__icontains=title) | Q(country__icontains=title) | Q(company_name__icontains=title)) 
        if (location != '') and (location is not None):
            queryset = queryset.filter(Q(location__icontains=location) | Q(country__icontains = location))
        if (full_time == 'true') and (full_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='full-time') | Q(job_type__icontains = 'Full_time'))
        if (part_time == 'true') and (part_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='part-time') | Q(job_type__icontains = 'part_time'))

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
        queryset = WorkDetails.objects.filter(country=company)
        keys = Job_keys.objects.filter(name__icontains = title)
        if (title != '') and (title is not None):
            queryset = queryset.filter(Q(job_title__icontains = title) | Q(job_keys__in = [key.id for key in keys]) | Q(location__icontains=title) | Q(country__icontains=title) | Q(company_name__icontains=title)) 
        if (location != '') and (location is not None):
            queryset = queryset.filter(Q(location__icontains=location) | Q(country__icontains = location))
        if (full_time == 'true') and (full_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='full-time') | Q(job_type__icontains = 'Full_time'))
        if (part_time == 'true') and (part_time is not None):
            queryset = queryset.filter(Q(job_type__icontains='part-time') | Q(job_type__icontains = 'part_time'))

        if ((interns == 'true') and (interns is not None)):
            queryset = queryset.filter(job_type__icontains='Internship')

        if ((contract == 'true') and (contract is not None)):
            queryset = queryset.filter(job_type__icontains='Contractor')
        return queryset

def blog(request):
    return render(request, 'blog.html')

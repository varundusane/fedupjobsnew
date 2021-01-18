from schedule import Scheduler
import threading
import time
from .models import JobCategory,WorkDetails
import requests
import os
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def weworkSrcipe():
    url = "https://weworkremotely.com/remote-jobs/search?term=remote"
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    section = soup.find_all("section", {"class": "jobs"})
    for item in section:
        a = item.select("li > a")
        for item2 in a:
            if str(item2.parent['class']) != "['view-all']":
                link = f"https://weworkremotely.com{item2.get('href')}"
                htmll = requests.get(link, headers=headers).text
                soupp = BeautifulSoup(htmll, 'lxml')
                des = soupp.find("div", {"class": "listing-container"})
                try:
                    company_logo = soupp.find_all('div', {"class": "listing-logo"})[0].find('img', src=True)
                except IndexError:
                    continue
                posted_on = soupp.find('div', {'class': 'listing-header-container'})
                try:
                    posted_on = posted_on.find('h3').get_text()
                except:
                    posted_on = ''
                apply_link_div = soupp.find_all('div', {'class': 'apply_tooltip'})[0].find('a', href=True)
                apply_links  = apply_link_div['href'] # HERE IS THE APPLYABLE LINK #############
                company = item2.find("span", {"class": "company"})
                title = item2.find("span", {"class": "title"})
            else:
                continue
            try:
                category = JobCategory.objects.all().first()
            except:
                category = JobCategory(name = 'Recent')
                category.save()
            job = WorkDetails(category=category, job_title=title.get_text(),posted_on=posted_on, job_desc=des.text.strip(), apply_job_link=apply_links, company_name=company.get_text(),  is_scraped_data=True, company_img_url=company_logo['src']
            )

            job.save()



def start_stackoverflow_scrapes():
    url = f"https://stackoverflow.com/jobs?r=true&q=devops"

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    company = soup.find_all("h3", {"class": "fc-black-700 fs-body1 mb4"})
    for item in company:
        company_name = item.find("span")
        items = soup.find_all("a", {"class": "s-link stretched-link"})
        for item in items:
            company_names = company_name.get_text().strip()
            title_text = item.get_text()
            link2 = f"https://stackoverflow.com{item.get('href')}"
            
            htmll = requests.get(link2, headers=headers).text
            soupp = BeautifulSoup(htmll, 'lxml')
            des = soupp.find("section", {"class": "mb32 fs-body2 fc-medium pr48"})
            time_of_post = soupp.find('ul', {"class" : "horizontal-list horizontal-list__lg fs-body1 fc-black-500 ai-baseline mb24"})
            try:
                posted_on = time_of_post.find('li').get_text()
            except:
                posted_on = ''
            apply_link = soupp.find_all('div', {'class': "js-apply-container"})[1].find('a', href=True)
            the_apply_link = apply_link['href'] # HERE IS THE APPLICABLE LINKS
            company_logo = soupp.find('div', {'class': 'grid--cell fl-shrink0'}).find('img', src=True)
            try:
                category = JobCategory.objects.all().first()
            except:
                category = JobCategory(name = 'Recent')
                category.save()
            job = WorkDetails(
                category=category, job_title=title_text,posted_on=posted_on, job_desc=des.text.strip(), apply_job_link=the_apply_link, company_name=company_names,  is_scraped_data=True, company_img_url=company_logo['src']
            )
            job.save()



def joson_response():
    remoteok = 'https://remoteok.io/api'
    result2 = requests.get(remoteok, headers=headers)
    responses = result2.json()
    try:
        category = JobCategory.objects.all().first()
    except:
        category = JobCategory(name = 'Recent')
        category.save()
    for response in responses:
        try:
            job = WorkDetails(category=category, job_title=response['position'], posted_on=response['date'], job_desc=response['description'], apply_job_link=response['url'], company_name=response['company'],  is_scraped_data=True, company_img_url=response['company_logo']
                )
            job.save()
        except:
            pass

def Command():
        # JobCategory.objects.all()
        WorkDetails.objects.filter(is_scraped_data=True).delete()
        print('Called')
        weworkSrcipe()
        start_stackoverflow_scrapes()
        joson_response()






def run_continuously(self, interval=5):
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
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously   

def start_scheduler():
    scheduler = Scheduler()
    scheduler.every().second.do(Command)
    scheduler.run_continuously()     


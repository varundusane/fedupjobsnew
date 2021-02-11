from schedule import Scheduler
import threading
import time
from .models import JobCategory, WorkDetails
import requests
import os
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


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
                desc = str(des)
                print(desc)
                # p = des.find_all("div")
                # paragraphs = []
                #
                # for x in p:
                #     paragraphs.append(str(x))
                #
                # print(paragraphs)
                # stri = ""
                # for pa in paragraphs:
                #     stri += pa
                # f = open('templates/created.html', 'w')
                #
                # f.write(stri)
                # f.close()
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
                apply_links = apply_link_div['href']  # HERE IS THE APPLYABLE LINK #############
                company = item2.find("span", {"class": "company"})
                title = item2.find("span", {"class": "title"})
            else:
                continue
            try:
                category = JobCategory.objects.all().first()
            except:
                category = JobCategory(name='Recent')
                category.save()
            job = WorkDetails(category=category, job_title=title.get_text(), posted_on=posted_on,
                              job_desc=desc, apply_job_link=apply_links, company_name=company.get_text(),
                              is_scraped_data=True, company_img_url=company_logo['src'],
                              )

            job.save()


def start_stackoverflow_scrapes():
    title_texts = []

    descriptions = []
    jobs = []
    company_namess = []
    company_img = []

    url = f"https://stackoverflow.com/jobs?r=true"

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, features='html.parser')

    pages = soup.find("div", {"class": "s-pagination"}).find_all('a', {"class": "s-pagination--item"})
    pages.pop()
    # print(pages)
    for page in pages:
        print(page.text)
        if page.text != 'nextchevron_right':
            page_url = page['href']
            link1 = f"https://stackoverflow.com{page_url}"
            htmls = requests.get(link1, headers=headers).text
            soups = BeautifulSoup(htmls, features='html.parser')

            items = soups.find_all("a", {"class": "s-link stretched-link"})
            # print(len(items))
            for item in items:
                title_text = item.get_text()
                link2 = f"https://stackoverflow.com{item.get('href')}"

                htmll = requests.get(link2, headers=headers).text
                soupp = BeautifulSoup(htmll, features='html.parser')
                company_names = soupp.find('div', {'class': "fc-black-700 fs-body3"}).find('a')
                # print(company_names)
                des = soupp.find("section", {"class": "mb32 fs-body2 fc-medium pr48"})
                # print(des)
                desc = str(des)
                time_of_post = soupp.find('ul', {
                    "class": "horizontal-list horizontal-list__lg fs-body1 fc-black-500 ai-baseline mb24"})

                try:
                    posted_on = time_of_post.find('li').get_text()
                except:
                    posted_on = ''
                apply_link = soupp.find_all('div', {'class': "js-apply-container"})[1].find('a', href=True)
                try:
                    the_apply_link = apply_link['href']  # HERE IS THE APPLICABLE LINKS
                except:
                    continue
                company_logo = soupp.find('div', {'class': 'grid--cell fl-shrink0'}).find('img', src=True)
                try:
                    category = JobCategory.objects.all().first()
                except:
                    category = JobCategory(name='Recent')
                    category.save()
                try:
                    job = WorkDetails(
                        category=category, job_title=title_text, posted_on=posted_on, job_desc=desc,
                        apply_job_link=the_apply_link, company_name=company_names.text, is_scraped_data=True,
                        company_img_url=company_logo['src']
                    )
                    job.save()
                except:
                    pass


def joson_response():
    remoteok = 'https://remoteok.io/api'
    result2 = requests.get(remoteok, headers=headers)
    responses = result2.json()
    try:
        category = JobCategory.objects.all().first()
    except:
        category = JobCategory(name='Recent')
        category.save()
    for response in responses:
        try:
            job = WorkDetails(category=category, job_title=response['position'], posted_on=response['date'],
                              job_desc=response['description'], apply_job_link=response['url'],
                              company_name=response['company'], is_scraped_data=True,
                              company_img_url=response['company_logo']
                              )
            job.save()
        except:
            pass


def Command():
    print('Called')
    WorkDetails.objects.filter(is_scraped_data=True).delete()
    weworkSrcipe()
    start_stackoverflow_scrapes()
    joson_response()


def run_continuously(self, interval=7):
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

# Command()

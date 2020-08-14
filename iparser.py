import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import threading
from utils import regions
from utils import Vacancy
from datetime import datetime

from utils import Vacancy, time_track
import urllib3

urllib3.disable_warnings()


class IndeedParser(threading.Thread):

    def __init__(self, keywords, region, existing_vacancy_ids=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vacancies = []
        self.pagelinks = None
        self.keywords = keywords
        self.region = region
        self.base_url = "indeed.com"
        self.jobsearch_url = None  # "https://ru.indeed.com/jobs?"
        self.query = None
        self.location = None
        self.name = None
        self.joblist = []
        self.vacancy_texts = []
        self.existing_vacancy_ids = existing_vacancy_ids
        self.country = None

        if len(keywords) > 1:
            self.name = "_".join(keywords.strip().split(" "))
            self.keywords = "+".join(keywords.strip().split(" "))
        else:
            self.keywords = keywords.strip()
            self.name = keywords.strip()

        if region:
            self.region = region
            self.name += "_" + region
            if region in regions["de"]:
                self.country = "de"
                self.base_url = f"de.{self.base_url}"
                self.region = '+'.join(self.region.strip().split(" "))
                self.jobsearch_url = f"https://{self.base_url}/jobs?q={self.keywords}&l={self.region}"

            elif region in regions["ru"]:
                self.country = "ru"
                self.base_url = f"ru.{self.base_url}"
                self.region = '+'.join(self.region.strip().split(" "))
                self.jobsearch_url = f"https://{self.base_url}/jobs?q={self.keywords}&l={self.region}"

            elif region in regions["uk"]:
                self.country = "uk"
                self.base_url = "www.indeed.co.uk"
                self.region = '+'.join(self.region.strip().split(" "))
                self.jobsearch_url = f"https://{self.base_url}/jobs?q={self.keywords}&l={self.region}"

            elif region in regions["us"]:
                self.country = "us"
                self.base_url = "www.indeed.com"
                self.region = '+'.join(self.region.strip().split(" "))
                self.jobsearch_url = f"https://{self.base_url}/jobs?q={self.keywords}&l={self.region}"

        else:
            self.jobsearch_url = f"https://ru.indeed.com/jobs?q={self.keywords}"

    def _make_soup(self, url):
        """ Создает объект soup из ссылки """

        res = requests.get(url, verify=False)
        page = res.text
        soup = BeautifulSoup(page, "html.parser")
        return soup

    def _generate_pagination_links(self):
        """ Генерирует ссылки на списки с вакансиями по общему числу вакансий"""

        soup = self._make_soup(self.jobsearch_url)
        total_vacs = soup.find("div", {"id": "searchCountPages"}).text.strip().split(' ')[-2]
        total_vacs = int(total_vacs.replace(",", ""))
        generated_links = [self.jobsearch_url + f"&start={c}" for c in range(10, total_vacs, 10)]

        self.pagelinks = [self.jobsearch_url] + generated_links

        return self.pagelinks

    def _get_vacancy_pages(self, jobs_url):
        """ Получает список ссылок на вакансии """

        soup = self._make_soup(jobs_url)
        alinks = soup.find_all("a", class_="jobtitle turnstileLink")
        temp_joblist = []

        for link in alinks:
            # temp_joblist.append((link["title"], link["href"]))
            temp_joblist.append(link["href"])

        return temp_joblist

    def _get_vacancy_text(self, right_link_part):
        """ Получает текст вакансии """

        if right_link_part.startswith("https://"):
            vacancy_link = right_link_part
        else:
            vacancy_link = f"https://{self.base_url}{right_link_part}"
        # print(vacancy_link)
        # https://directtointerview.indeed.com/jobs/7c35f8b03338250d

        soup = self._make_soup(vacancy_link)
        try:
            page_content = soup.find("div", class_="jobsearch-jobDescriptionText").text
            page_content_html = str(soup.find("div", class_="jobsearch-jobDescriptionText"))
        except AttributeError:
            page_content = ""
            page_content_html = ""
        return page_content, page_content_html

    def run(self):
        """ Запускает парсер """

        print(self.jobsearch_url)
        joblist_pages = self._generate_pagination_links()

        self.list_of_vacancy_links = []

        for pager in joblist_pages:
            joblist_url = pager
            temp_list_of_vacancy_links = self._get_vacancy_pages(joblist_url)
            self.list_of_vacancy_links.extend(temp_list_of_vacancy_links)

        self.list_of_vacancy_links = list(set( self.list_of_vacancy_links))
        self._check_existing_vacancy_ids()

        c_date = datetime.today().strftime("%d-%m-%Y")
        reqs = ""
        skills = ""

        # print(self.list_of_vacancy_links)
        for vaclink in tqdm(self.list_of_vacancy_links):
            vac_text, vac_html = self._get_vacancy_text(vaclink)
            self.vacancy_texts.append(vac_text)
            vacobj = Vacancy(vaclink, vac_text, vac_html, self.keywords, self.country, self.region, reqs, skills, c_date)
            self.vacancies.append(vacobj)


    def _check_existing_vacancy_ids(self):
        """ Проверка на наличие распарсенной вакансии, оставляем только те, которых нет в списке """

        if self.existing_vacancy_ids:
            self.list_of_vacancy_links = list(
                set(self.list_of_vacancy_links).difference(set(self.existing_vacancy_ids)))

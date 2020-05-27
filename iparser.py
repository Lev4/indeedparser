import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import pickle
import threading
from utils import time_track
from utils import professions


class IndeedParser(threading.Thread):

    def __init__(self, keywords, region, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pagelinks = None
        self.keywords = keywords
        self.region = region
        self.base_url = "indeed.com"
        self.jobsearch_url = None # "https://ru.indeed.com/jobs?"
        self.query = None
        self.location = None
        self.name = None
        self.joblist = []
        self.vacancy_texts = []



        if len(keywords) > 1:
            self.name = "_".join(keywords.strip().split(" "))
            self.keywords = "+".join(keywords.strip().split(" "))
        else:
            self.keywords = keywords.strip()
            self.name = keywords.strip()

        if region:
            self.region = region
            self.name += "_" + region
            if region in ["Berlin"]:
                self.base_url = f"de.{self.base_url}"
                self.jobsearch_url = f"https://{self.base_url}/jobs?q={self.keywords}&l={self.region}"
            elif region in ["Москва",'Moscow']:
                self.base_url = f"ru.{self.base_url}"
                self.jobsearch_url = f"https://{self.base_url}/jobs?q={self.keywords}&l={self.region}"
            elif region in ["London"]:
                self.base_url = "www.indeed.co.uk"
                self.jobsearch_url = f"https://{self.base_url}/jobs?q={self.keywords}&l={self.region}"
        else:
            self.jobsearch_url = f"https://ru.indeed.com/jobs?q={self.keywords}"


    def _make_soup(self, url):
        """ Создает объект soup из ссылки """

        res = requests.get(url)
        page = res.text
        soup = BeautifulSoup(page, "html.parser")
        return soup

    def _generate_pagination_links(self):
        """ Генерирует ссылки на списки с вакансиями по общему числу вакансий"""

        soup = self._make_soup(self.jobsearch_url)
        total_vacs = soup.find("div", {"id": "searchCountPages"}).text.strip().split(' ')[-2]
        total_vacs = int(total_vacs)

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

        vacancy_link = "https://ru.indeed.com" + right_link_part
        soup = self._make_soup(vacancy_link)
        page_content = soup.find("div", class_="jobsearch-jobDescriptionText").text

        return page_content

    def run(self):
        """ Запускает парсер """

        print(self.jobsearch_url)
        joblist_pages = self._generate_pagination_links()

        self.list_of_vacancy_links = []

        for pager in joblist_pages:
            joblist_url = pager
            temp_list_of_vacancy_links = self._get_vacancy_pages(joblist_url)
            self.list_of_vacancy_links.extend(temp_list_of_vacancy_links)

        self.list_of_vacancy_links = list(set(self.list_of_vacancy_links))

        for vaclink in tqdm(self.list_of_vacancy_links):
            vac_text = self._get_vacancy_text(vaclink)
            self.vacancy_texts.append(vac_text)


@time_track
def main():

    parsed_dict = {prof: IndeedParser(keywords=prof, region="Moscow") for prof in professions["ru"]}
    for prof_parser in parsed_dict.values():
        prof_parser.start()
    for prof_parser in parsed_dict.values():
        prof_parser.join()

    vacs_dict = {}
    for k, v in parsed_dict.items():
        vacs_dict[k] = v.vacancy_texts

    with open("vacs_dict.pkl", "wb") as f:
        pickle.dump(vacs_dict, f)


if __name__ == '__main__':
    main()

import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import pickle


class IndeedParser:

    def __init__(self):
        self.pagelinks = None
        self.keywords = None
        self.region = None
        self.jobsearch_url = "https://ru.indeed.com/jobs?"
        self.query = None
        self.location = None
        self.joblist = []
        self.vacancy_texts = []

    def _make_soup(self, url):
        """ Создает объект soup из ссылки """

        res = requests.get(url)
        page = res.text
        soup = BeautifulSoup(page, "html.parser")
        return soup

    def generate_pagination_links(self):
        """ Генерирует ссылки на списки с вакансиями по общему числу вакансий"""

        soup = self._make_soup(self.jobsearch_url)
        total_vacs = soup.find("div", {"id": "searchCountPages"}).text.strip().split(' ')[-2]
        total_vacs = int(total_vacs)

        generated_links = [self.jobsearch_url + f"&start={c}" for c in range(10, total_vacs, 10)]

        self.pagelinks = [self.jobsearch_url] + generated_links

        return self.pagelinks

    def get_vacancy_pages(self, jobs_url):
        """ Получает список ссылок на вакансии """

        soup = self._make_soup(jobs_url)
        alinks = soup.find_all("a", class_="jobtitle turnstileLink")
        temp_joblist = []

        for link in alinks:
            # temp_joblist.append((link["title"], link["href"]))
            temp_joblist.append(link["href"])

        return temp_joblist

    def get_vacancy_text(self, right_link_part):
        """ Получает текст вакансии """

        vacancy_link = "https://ru.indeed.com" + right_link_part
        soup = self._make_soup(vacancy_link)
        page_content = soup.find("div", class_="jobsearch-jobDescriptionText").text

        return page_content

    def fit(self, keywords, region):
        """ Собирает все по заданным ключевым словам """

        if len(keywords) > 1:
            self.keywords = "+".join(keywords.strip().split(" "))
        else:
            self.keywords = keywords.strip()

        if region:
            self.region = region
            self.jobsearch_url = f"https://ru.indeed.com/jobs?q={self.keywords}&l={self.region}"
        else:
            self.jobsearch_url = f"https://ru.indeed.com/jobs?q={self.keywords}"
        return self.jobsearch_url

    def run(self):
        """ Запускает парсер """

        print(self.jobsearch_url)
        joblist_pages = self.generate_pagination_links()

        self.list_of_vacancy_links = []

        for pager in joblist_pages:
            joblist_url = pager
            temp_list_of_vacancy_links = self.get_vacancy_pages(joblist_url)
            self.list_of_vacancy_links.extend(temp_list_of_vacancy_links)

        self.list_of_vacancy_links = list(set(self.list_of_vacancy_links))

        for vaclink in tqdm(self.list_of_vacancy_links):
            vac_text = self.get_vacancy_text(vaclink)
            self.vacancy_texts.append(vac_text)


if __name__ == '__main__':

    professions = [
        "Java разработчик ",
        "Software engineer",
        "Web разработчик",
        "Front-end разработчик",
        "Продуктовый дизайнер",
        "Системный аналитик",
        "Архитектор систем",
        "Agile coach",
        "Data Scientist",
        "Data engineer",
        "Бизнес-аналитик",
        "Финансовый аналитик",
        "Кредитный аналитик",
        "Юрист корпоративный",
        "Юрист судебный",
        "Маркетолог",
    ]

    vacancy_dict = {}
    for prof in tqdm(professions):
        print(prof)
        p = IndeedParser()
        p.fit(keywords=prof, region="Moscow")
        p.run()
        vacancy_dict[prof] = p.vacancy_texts

    # with open("vacs_dict.pkl", "wb") as f:
    #     pickle.dump(vacancy_dict, f)

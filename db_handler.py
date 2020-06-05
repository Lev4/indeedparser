import sqlite3

from utils import Vacancy

vacancy_db = "vacancies.sqlite3"


# Vacancy = namedtuple('Vacancy', [
#     'vacancy_id',
#     'vacancy_description',
#     'profession'
#     'country',
#     'city',
#     'requirements',
#     'skills',
#     'parsing_date',
# ])


class Db_handler:

    def __init__(self, db):
        self.db = db

    def _stmt_executer(self, query, get_data=False):
        con = sqlite3.connect(self.db)
        c = con.cursor()
        if get_data:
            data_result = c.execute(query).fetchall()
            con.commit()
            con.close()

            return data_result
        else:
            c.execute(query)
            con.commit()
            con.close()

    def create_tab(self):

        stmt = """
        CREATE TABLE IF NOT EXISTS vacancies_tab
              (vacancy_id text,
               vacancy_description text,
               profession text,
               country text,
               city text, 
               requirements text, 
               skills text, 
               parsing_date text);
        """
        self._stmt_executer(stmt)

    def addvacancy(self, Vacancy):
        stmt = f""" INSERT INTO prices ('vacancy_id',
                                      'vacancy_description',
                                      'profession', 
                                      'country',
                                      'city',
                                      'requirements', 
                                      'skills',
                                      'parsing_date') 
                    VALUES ('{Vacancy.vacancy_id}',
                            '{Vacancy.vacancy_description}', ,
                            '{Vacancy.profession}',
                            '{Vacancy.country}',
                            '{Vacancy.city}',
                            '{Vacancy.requirements}',
                            '{Vacancy.skills}',
                            '{Vacancy.parsing_date}'),
                            ) """
        self._stmt_executer(stmt)

    def update_vacancy(self, cheese_id, price):
        stmt = f"UPDATE prices SET price = {price} WHERE cheese_id = {cheese_id} "
        self._stmt_executer(stmt)

    def show_vacancies(self):
        stmt = f"SELECT * FROM vacancies_tab"
        return self._stmt_executer(stmt, get_data=True)

    def show_vacancies_by_date(self, target_date):
        stmt = f"SELECT * FROM vacancies_tab WHERE parsing_date = '{target_date}'"
        return self._stmt_executer(stmt, get_data=True)



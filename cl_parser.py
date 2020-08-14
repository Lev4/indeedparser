import pickle
import db_handler
from utils import time_track
from utils import professions
from utils import get_location_from_args
from datetime import datetime
from iparser import IndeedParser
from utils import regions

regionslist = regions["uk"] + regions["us"]

@time_track
def main():

    vacancy_db = "vacancies_html.sqlite3"
    db = db_handler.Db_handler(vacancy_db)
    db.create_tab()


    for city in regionslist:
        # location = get_location_from_args()
        v_ids = [x[0] for x in db.show_vacancy_ids()]

        if len(v_ids) == 0:
            v_ids = None

        location = city
        if location:
            parsed_dict = {prof: IndeedParser(keywords=prof, region=location, existing_vacancy_ids=v_ids) for prof in professions["en"]}
        else:
            parsed_dict = {prof: IndeedParser(keywords=prof, existing_vacancy_ids=v_ids) for prof in professions["en"]}

        for prof_parser in parsed_dict.values():
            prof_parser.start()
        for prof_parser in parsed_dict.values():
            prof_parser.join()

        vacs_dict = {}
        for k, v in parsed_dict.items():
            vacs_dict[k] = v.vacancy_texts

        for v in parsed_dict.values():
            for vaca in v.vacancies:
                db.addvacancy(vaca)


    print(f"{'*' * 10} Удалось найти: {'*' * 10}")
    for k, v in vacs_dict.items():
        print(f"{k} - {len(v)} вакансий")
    print(f"{'*' * 30}")

    # current_date = datetime.today().strftime("%d-%m-%Y")
    # with open(f"dallas_{current_date}.pkl", "wb") as f:
    # pickle.dump(vacs_dict, f)

if __name__ == '__main__':
    main()

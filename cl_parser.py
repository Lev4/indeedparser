import pickle
from utils import time_track
from utils import professions
from utils import get_location_from_args
from datetime import datetime, timedelta



@time_track
def main():
    location = get_location_from_args()
    if location:
        parsed_dict = {prof: IndeedParser(keywords=prof, region="Dallas") for prof in professions["en"]}
    else:
        parsed_dict = {prof: IndeedParser(keywords=prof) for prof in professions["en"]}

    for prof_parser in parsed_dict.values():
        prof_parser.start()
    for prof_parser in parsed_dict.values():
        prof_parser.join()

    vacs_dict = {}
    for k, v in parsed_dict.items():
        vacs_dict[k] = v.vacancy_texts
    print(f"{'*' * 10} Удалось найти: {'*' * 10}")
    for k, v in vacs_dict.items():
        print(f"{k} - {len(v)} вакансий")
    print(f"{'*' * 30}")

    current_date = datetime.today().strftime("%d-%m-%Y")
    with open(f"dallas_{current_date}.pkl", "wb") as f:
        pickle.dump(vacs_dict, f)


if __name__ == '__main__':
    main()
